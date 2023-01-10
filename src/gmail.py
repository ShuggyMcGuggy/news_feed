import smtplib
import ssl

def send_email(body_text="No Body"):
    ctx = ssl.create_default_context()
    password = "Shelleligh324(<Yak"  # Your app password goes here
    sender = "markss@markshury-smith.in"  # Your e-mail address
    receiver = "mark.shury.smith@me.com"  # Recipient's address
    message = """\
    From: "Mark Shury-Smith" <markss@markshury-smith.in>
    To: "Me" <mark.shury.smith@me.com>
    Subject: Emails from Commentator


    The News feed refresh batch job has executed successfully
    

    """ + body_text


    with smtplib.SMTP_SSL("smtp.titan.email", port=465, context=ctx) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)


#     ctx = ssl.create_default_context()
#     # password = "Phfevktksutcouoz"  # Your app password goes here
#     # sender = "shurysmithmark@gmail.com"  # Your e-mail address
#     password = "Shelleligh324(<Yak"  # Your app password goes here
#     sender = "markss@markshury-smith.in"  # Your e-mail address
#     receiver = "mark.shury.smith@me.com"  # Recipient's address
#     message = """\
#     From: "Mark Shury-Smith" <markss@markshury-smith.in>
#     To: "Me" <mark.shury.smith@me.com>
#     Subject: Emails for Commentator
#
#
#     Looks like we have this email stuff sussed:  Yay!
#     Now to get this working with commentator
#
#     """
#
#     # with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
#     #     server.login(sender, password)
#     #     server.sendmail(sender, receiver, message)
#
#     with smtplib.SMTP_SSL("smtp.titan.email", port=465, context=ctx) as server:
#         server.login(sender, password)
#         server.sendmail(sender, receiver, message)
#
#  # ---------
#
# ctx = ssl.create_default_context()
# password = "Shelleligh324(<Yak"  # Your app password goes here
# sender = "markss@markshury-smith.in"  # Your e-mail address
# receiver = "mark.shury.smith@me.com" # Recipient's address
# message = """\
# From: "Mark Shury-Smith" <markss@markshury-smith.in>
# To: "Me" <mark.shury.smith@me.com>
# Subject: Emails for Commentator
#
#
# Looks like we have this email stuff sussed:  Yay!
# Now to get this working with commentator
#
# """
#
# with smtplib.SMTP_SSL("smtp.titan.email", port=465, context=ctx) as server:
#     server.login(sender, password)
#     server.sendmail(sender, receiver, message)