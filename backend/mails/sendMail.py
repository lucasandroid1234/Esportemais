#Back-end/mails/sendMail.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mails.infoMail import InfoMail, Config

def send_email(user_info):
    server = None
    server_smtp = Config.CONECTION
    port = Config.PORT
    sender_email = Config.MAIL
    password = Config.MAIL_PASSWORD
    receive_email = user_info.email
    subject = 'Cadastro Esporte+!'

    body = InfoMail.EmailCadastro(user_info.nome)

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receive_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP(server_smtp, port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receive_email, message.as_string())
    except Exception:
        print("Erro: Endereço de E-mail Inválido")
    finally:
        if server:
            server.quit()

def send_email_reset_password(email, nome, token: str):
    server = None
    server_smtp = Config.CONECTION
    port = Config.PORT
    sender_email = Config.MAIL
    password = Config.MAIL_PASSWORD
    receive_email = email
    body = InfoMail.EmailRedefinicaoSenha(nome, token)
    subject = 'Redefinição de Senha Esporte+!'

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receive_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP(server_smtp, port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receive_email, message.as_string())
    except Exception:
        print("Erro: Endereço de E-mail Inválido")
    finally:
        if server:
            server.quit()

def send_email_agendamento(email, nome, agendamento):
    server = None
    server_smtp = Config.CONECTION
    port = Config.PORT
    sender_email = Config.MAIL
    password = Config.MAIL_PASSWORD
    receive_email = email
    body = InfoMail.EmailConfirmacaoAgendamento(nome, agendamento)
    subject = 'Confirmação de Agendamento!'

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receive_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP(server_smtp, port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receive_email, message.as_string())
    except Exception:
        print("Erro: Endereço de E-mail Inválido")
    finally:
        if server:
            server.quit()

def send_email_cancelamento_agendamento(email, nome, agendamento): 
    server = None
    server_smtp = Config.CONECTION
    port = Config.PORT
    sender_email = Config.MAIL
    password = Config.MAIL_PASSWORD
    receive_email = email
    body = InfoMail.EmailCancelamentoAgendamento(nome, agendamento)
    subject = 'Cancelamento de Agendamento!'

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receive_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP(server_smtp, port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receive_email, message.as_string())
    except Exception:
        print("Erro: Endereço de E-mail Inválido")
    finally:
        if server:
            server.quit()