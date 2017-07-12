# TODO Make image clickable in signature
# TODO Make dynamic and not company specific
# TODO Write email parser script so someone can send me an email with their info and it will auto make them a signature

# Create a ?.htm file for Outlook signature.
# Takes parameters: FirstName, LastName, Title, EmailAddress, WorkPhone, CellPhone, LinkToCustomImage

# Original html output
# <table cellpadding="0" cellspacing="0" border="0" style="background: none; border-width: 0px; border: 0px; margin: 0; padding: 0;">
# <tr><td colspan="2" style="padding-bottom: 5px; color: #159558; font-size: 18px; font-family: Arial, Helvetica, sans-serif;">NAME</td></tr>
# <tr><td colspan="2" style="color: #333333; font-size: 14px; font-family: Arial, Helvetica, sans-serif;"><i>TITLE</i></td></tr>
# <tr><td colspan="2" style="color: #333333; font-size: 14px; font-family: Arial, Helvetica, sans-serif;"><strong>COMPANY</strong></td></tr>
# <tr><td width="20" valign="top" style="vertical-align: top; width: 20px; color: #159558; font-size: 14px; font-family: Arial, Helvetica, sans-serif;">W:</td><td valign="top" style="vertical-align: top; color: #333333; font-size: 14px; font-family: Arial, Helvetica, sans-serif;">WORKPHONE&nbsp;&nbsp;<span style="color: #159558;">M:&nbsp;</span>CELLPHONE</td></tr>
# <tr><td width="20" valign="top" style="vertical-align: top; width: 20px; color: #159558; font-size: 14px; font-family: Arial, Helvetica, sans-serif;">w:</td><td valign="top" style="vertical-align: top; color: #333333; font-size: 14px; font-family: Arial, Helvetica, sans-serif;"><a href="WEBSITELINK" style=" color: #1da1db; text-decoration: none; font-weight: normal; font-size: 14px;">WEBSITE</a>&nbsp;&nbsp;<span style="color: #159558;">e:&nbsp;</span><a href="mailto:EMAILADDRESSLINK" style="color: #1da1db; text-decoration: none; font-weight: normal; font-size: 14px;">EMAILADDRESS</a></td></tr>
# <tr><td colspan="2" style="padding-bottom: 8px; padding-top: 5px;"><a href="SIGNATUREIMAGELINK"><img src="SIGNATUREIMAGELINK"></a></td></tr>
# </table>

from sys import argv
import argparse

# Default URL for image
DEFAULTURL = "http://easypayfinance.com/Cdn/Images/epf_logo_sm.png"
DEFAULTWEBSITE = "https://easypayfinance.com"
DEFAULTFILEPATH = "./Signature.htm"


# Gets user info from terminal and returns a dictionary.
def getUserInfo(info=None):
    global DEFAULTURL

    if info is None:
        info = dict.fromkeys([
            "firstname",
            "lastname",
            "title",
            "emailaddress",
            "workphone",
            "cellphone",
            "linkaddress",
            "filepath"
            "websitelink"
            ])

    elif info["noprompt"] is True:
        info["linkaddress"] = DEFAULTURL
        info["websitelink"] = DEFAULTWEBSITE
        info["filepath"] = DEFAULTFILEPATH
        return info

    if not info["firstname"]:
        info["firstname"] = input("Enter First Name: ")
    if not info["lastname"]:
        info["lastname"] = input("Enter Last Name: ")
    if not info["title"]:
        info["title"] = input("Enter Title: ")
    if not info["emailaddress"]:
        info["emailaddress"] = input("Enter Email Address: ")
    if not info["workphone"]:
        info["workphone"] = input("Enter Work Phone Number: ")
    if not info["cellphone"]:
        info["cellphone"] = input("Enter Cell Phone Number: ")
    if not info["linkaddress"]:
        temp = input("Enter URL link to custom image (Press Enter for Default): ")
        if temp == '':
            info["linkaddress"] = DEFAULTURL
        else:
            info["linkaddress"] = str(temp)
    if not info["filepath"]:
        temp = input("Enter filename and path to write to (Press Enter for Default - ./Signature.html):")
        if temp == '':
            info["filepath"] = DEFAULTFILEPATH
        else:
            info["filepath"] = str(temp)


    if not info["websitelink"]:
        temp = input("Enter the address of your website:")
        if temp == '':
            info["websitelink"] = DEFAULTWEBSITE
        else:
            info["websitelink"] = str(temp)

    return info


def parseArguments():
    global DEFAULTURL

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--firstname", help="Your First Name")
    parser.add_argument("-l", "--lastname", help="Your Last Name")
    parser.add_argument("-t", "--title", help="Your Title")
    parser.add_argument("-e", "--emailaddress", help="Your Email Address")
    parser.add_argument("-w", "--workphone", help="Your Work Phone")
    parser.add_argument("-c", "--cellphone", help="Your Cell Phone")
    parser.add_argument("-a", "--linkaddress", help="URL to a custom signature image")
    parser.add_argument("-p", "--filepath", help="Filepath and name of file to write to (ex: C:/Users/FlashGordon/Documents/ImASignature.html)")
    parser.add_argument("-s", "--websitelink", help="Website address for the image link")
    parser.add_argument("-x", "--noprompt", action="store_true", help="Run silently")

    return vars(parser.parse_args())


def makeHTML(info):
    print (info["filepath"])
    file = open(info["filepath"], 'w')

    html_str = """<!DOCTYPE html>"""
    html_str += """\n<table cellpadding="0" cellspacing="0" border="0" style="background: none; border-width: 0px; border: 0px; margin: 0; padding: 0;">"""
    html_str += """\n<tr><td colspan="2" style="padding-bottom: 5px; color: #159558; font-size: 18px; font-family: Arial, Helvetica, sans-serif;">%s %s</td></tr>""" % (info["firstname"], info["lastname"])
    if info["title"]:
        html_str += """\n<tr><td colspan="2" style="color: #333333; font-size: 14px; font-family: Arial, Helvetica, sans-serif;"><i>%s</i></td></tr>""" % (info["title"])

    temp = None
    if info["workphone"]:
        temp = """\n<tr><td width="20" valign="top" style="vertical-align: top; width: 20px;"><span style="color: #159558; font-size: 14px; font-family: Arial, Helvetica, sans-serif;">W:&nbsp</span>%s</td></tr>""" % (info["workphone"])
    if info["cellphone"]:
        temp = temp[:-10] + """&nbsp;&nbsp;<span style="color: #159558;">M:&nbsp;</span>%s</td></tr>""" % (info["cellphone"])
    if temp:
        html_str += temp

    if info["emailaddress"]:
        html_str += """\n<tr><td valign="top" style="vertical-align: top; color: #333333; font-size: 14px; font-family: Arial, Helvetica, sans-serif;"><span style="color: #159558;">E:&nbsp;</span><a href="mailto:%s" style="color: #1da1db; text-decoration: none; font-weight: normal; font-size: 14px;">%s</a></td></tr>""" % (info["emailaddress"], info["emailaddress"])

    html_str += """\n<tr><td colspan="2" style="padding-bottom: 8px; padding-top: 5px;"><a href="%s"><img src="%s"></a></td></tr>""" % (info["websitelink"],info["linkaddress"])
    html_str += """\n</table>"""

    file.write(html_str)


def tester():
    if len(argv) > 1 and '-' not in argv[0]:
        makeHTML(getUserInfo(parseArguments()))
    else:
        makeHTML(getUserInfo())


tester()


def main():
    if len(argv) > 1 and '-' not in argv[0]:
        parseArguments()
        print(getUserInfo(parseArguments()))
    else:
        print(getUserInfo())


# main()