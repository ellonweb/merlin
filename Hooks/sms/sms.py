# This file is part of Merlin.
# Merlin is the Copyright (C)2008,2009,2010 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
 
import json
import re
import socket
import time
from smtplib import SMTP, SMTPException, SMTPSenderRefused, SMTPRecipientsRefused
from ssl import SSLError
from urllib import urlencode
from urllib2 import urlopen, Request, URLError
from Core.exceptions_ import SMSError
from Core.config import Config
from Core.string import decode, encode
from Core.db import session
from Core.maps import User, SMS
from Core.loadable import loadable, route, require_user

class sms(loadable):
    """Sends an SMS to the specified user. Your username will be appended to the end of each sms. The user must have their phone correctly added and you must have access to their number."""
    usage = " <nick> <message>"
    
    @route(r"(\S+)\s+(.+)", access = "member")
    @require_user
    def execute(self, message, user, params):
        
        rec = params.group(1)
        public_text = params.group(2) + ' - %s' % (user.name,)
        text = encode(public_text + '/%s' %(user.phone,))
        receiver=User.load(name=rec,exact=False)
        if not receiver:
            message.reply("Who exactly is %s?" % (rec,))
            return
        if receiver.smsmode == "Retard":
            message.reply("I refuse to talk to that incompetent retard. Check %s's mydef comment and use !phone show to try sending it using your own phone." %(receiver.name,))
            return 

        if not receiver.pubphone and user not in receiver.phonefriends:
            message.reply("%s's phone number is private or they have not chosen to share their number with you. Supersecret message not sent." % (receiver.name,))
            return

        if receiver.smsmode == "Email":
            mode = receiver.smsmode
            phone = receiver.email
        else:
            mode = Config.get("Misc", "sms")
            phone = self.prepare_phone_number(receiver.phone)
            if not phone or len(phone) <= 7:
                message.reply("%s has no phone number or their phone number is too short to be valid (under 6 digits). Super secret message not sent." % (receiver.name,))
                return

        if len(text) >= 160:
            message.reply("Max length for a text is 160 characters. Your text was %i characters long. Super secret message not sent." % (len(text),))
            return

        mode = receiver.smsmode or mode if mode == "combined" else mode
        mode = mode.lower()
        error = ""
        
        if mode == "email":
            error = self.send_email(user, receiver, public_text, phone, text)
        if mode == "googlevoice" or mode == "combined":
            error = self.send_googlevoice(user, receiver, public_text, phone, text)
        if mode == "clickatell" or (mode == "combined" and error is not None):
            error = self.send_clickatell(user, receiver, public_text, phone, text)
        
        if error is None:
            message.reply("Successfully processed To: %s Message: %s" % (receiver.name, decode(text)))
        else:
            message.reply(error or "That wasn't supposed to happen. I don't really know what went wrong. Maybe your mother dropped you.")
    
    def send_clickatell(self, user, receiver, public_text, phone, message):
        try:
            # HTTP POST
            post = urlencode({"user"        : Config.get("clickatell", "user"),
                              "password"    : Config.get("clickatell", "pass"),
                              "api_id"      : Config.get("clickatell", "api"),
                              "to"          : phone,
                              "text"        : message,
                            })
            # Send the SMS
            status, msg = urlopen("https://api.clickatell.com/http/sendmsg", post, 5).read().split(":")
            
            # Check returned status for error messages
            if status in ("OK","ID",):
                self.log_message(user, receiver, phone, public_text, "clickatell")
                return None
            elif status in ("ERR",):
                raise SMSError(msg.strip())
            else:
                return ""
            
        except (URLError, SSLError, SMSError) as e:
            return "Error sending message: %s" % (str(e),)
    
    def send_googlevoice(self, user, receiver, public_text, phone, message):
        try:
            # HTTP POST
            post = urlencode({"accountType" : "GOOGLE",
                              "Email"       : Config.get("googlevoice", "user"),
                              "Passwd"      : Config.get("googlevoice", "pass"),
                              "service"     : "grandcentral",
                              "source"      : "Merlin",
                            })
            # Authenticate with Google
            text = urlopen("https://www.google.com/accounts/ClientLogin", post, 5).read()
            m = re.search(r"^Auth=(.+?)$", text, re.M)
            if m is None:
                raise SMSError("unable to authenticate")
            auth = m.group(1)
            
            # HTTP POST
            post = urlencode({"id"          : '',
                              "phoneNumber" : phone,
                              "text"        : message,
                              "auth"        : auth,
                              "_rnr_se"     : Config.get("googlevoice", "api"),
                            })
            # Send the SMS
            req = Request("https://www.google.com/voice/sms/send/")
            req.add_header('Authorization', "GoogleLogin auth="+auth)
            text = urlopen(req, post, 5).read()
            if text != '{"ok":true,"data":{"code":0}}':
                raise SMSError("success code not returned")
            
            # Allow a small amount of time for the request to be processed
            time.sleep(5)
            
            # HTTP GET
            get = urlencode({"auth"         : auth,
                           })
            # Request the SMS inbox feed
            req = Request("https://www.google.com/voice/inbox/recent/sms/?"+get)
            req.add_header('Authorization', "GoogleLogin auth="+auth)
            text = urlopen(req, None, 5).read()
            
            # Parse the feed and extract JSON data
            m = re.search(self.googlevoice_regex_json(), text)
            if m is None:
                raise SMSError("json data not found in feed")
            data = json.loads(m.group(1))
            for conversation in data['messages'].values():
                # One of the conversations should match
                #  the phone number we just tried SMSing
                if conversation['phoneNumber'] == phone:
                    id = conversation['id']
                    read = conversation['isRead']
                    
                    # Parse the feed and extract the relevant conversation
                    m = re.search(self.googlevoice_regex_conversation(id, read), text, re.S)
                    if m is None:
                        raise SMSError("conversation not found in SMS history")
                    
                    # Parse the conversation and extract the message
                    m = re.search(self.googlevoice_regex_message(message), m.group(1))
                    if m is None:
                        #raise SMSError("message not found in conversation")
                        continue
                    
                    # Check the message for error replies
                    if m.group(4) is None:
                        self.log_message(user, receiver, phone, public_text, "googlevoice")
                        return None
                    else:
                        return m.group(4)
                    
            else:
                raise SMSError("message not found in any of the matching conversations")
            
        except (URLError, SSLError, SMSError) as e:
            return "Error sending message: %s" % (str(e),)
    
    def googlevoice_regex_json(self):
        regex = r'<json><!\[CDATA\[(.*?)\]\]></json>'
        return regex
    
    def googlevoice_regex_conversation(self, id, read):
        regex = r'<div id="'+id+'"\s*class="goog-flat-button gc-message gc-message-'+ ('read' if read else 'sms') +'">'
        regex+= r'(.*?)'
        regex+= r'(?:class="goog-flat-button gc-message|$)'
        return regex
    
    def googlevoice_regex_message(self, message):
        message = re.escape(message)
        regex = r'<div class="gc-message-sms-row">\s*'
        regex+= r'<span class="gc-message-sms-from">\s*'
        regex+= r'Me:\s*'
        regex+= r'</span>\s*'
        regex+= r'<span class="gc-message-sms-text">\s*'
        regex+= r'('+message+')'
        regex+= r'</span>\s*'
        regex+= r'<span class="gc-message-sms-time">\s*'
        regex+= r'(.+?)\s*'
        regex+= r'</span>\s*'
        regex+= r'</div>\s*'
        regex+= r'(?:'
        regex+= r'<div class="gc-message-sms-row">\s*'
        regex+= r'<span class="gc-message-sms-from">\s*'
        regex+= r'(.*?):\s*'
        regex+= r'</span>\s*'
        regex+= r'<span class="gc-message-sms-text">\s*'
        regex+= r'(Error: this message was not successfully delivered.)'
        regex+= r'</span>\s*'
        regex+= r'<span class="gc-message-sms-time">\s*'
        regex+= r'(.*?)'
        regex+= r'</span>\s*'
        regex+= r'</div>\s*'
        regex+= r')?'
        return regex
    
    def prepare_phone_number(self,text):
        if not text:
            return text
        s = "".join([c for c in text if c.isdigit()])
        return "+"+s.lstrip("00")

    def send_email(self, user, receiver, public_text, email, message):
        try:
            smtp = SMTP(Config.get("smtp", "host"), Config.get("smtp", "port"))
            
            try:
                smtp.starttls()
            except SMTPException as e:
                raise SMSError("unable to shift connection into TLS: %s" % (str(e),))
            
            try:
                smtp.login(Config.get("smtp", "user"), Config.get("smtp", "pass"))
            except SMTPException as e:
                raise SMSError("unable to authenticate: %s" % (str(e),))
            
            try:
                smtp.sendmail(Config.get("smtp", "user"), email, 
                              "To:%s\nFrom:%s\nSubject:%s\n%s\n" % (email,
                                                                    Config.get("smtp", "user"),
                                                                    Config.get("Alliance", "name"),
                                                                    message,))
            except SMTPSenderRefused as e:
                raise SMSError("sender refused: %s" % (str(e),))
            except SMTPRecipientsRefused as e:
                raise SMSError("unable to send: %s" % (str(e),))
            
            smtp.quit()
            self.log_message(user, receiver, email, public_text, "email")
            
        except (socket.error, SSLError, SMTPException, SMSError) as e:
            return "Error sending message: %s" % (str(e),)
    
    def log_message(self,sender,receiver,phone,text,mode):
        session.add(SMS(sender=sender,receiver=receiver,phone=phone,sms_text=text,mode=mode))
        session.commit()
