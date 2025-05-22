#Back-end/mails/infoMail.py

from dotenv import load_dotenv
import os
load_dotenv()  

class Config:
    CONECTION = os.getenv("CONECTION")
    PORT = os.getenv("PORT")
    MAIL = os.getenv("MAIL")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")


class InfoMail:

    def EmailCadastro(nome):
        body = f"""
            <html lang="pt-BR">
                <head>
                    <meta charset="UTF-8">
                    <title>Cadastro Confirmado</title>
                </head>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <h2>Cadastro confirmado!</h2>
                    <p>Olá <strong>{nome}</strong>,</p>
                    <p>Seu cadastro no sistema <strong>Esporte+</strong> foi realizado com sucesso.</p>
                    <p>Agora você pode acessar o sistema e começar a agendar suas quadras esportivas.</p>
                    <p>Obrigado por se cadastrar!</p>
                    <br>
                    <p>Atenciosamente,<br>Equipe Esporte+</p>
                </body>
            </html>
        """
        return body

    def EmailRedefinicaoSenha(nome, token):
        body = f"""
            <html lang="pt-BR">
                <head>
                    <meta charset="UTF-8">
                    <title>Redefinição de Senha</title>
                </head>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <h2>Redefinição de Senha</h2>
                    <p>Olá <strong>{nome}</strong>,</p>
                    <p>Recebemos um pedido para redefinir sua senha.</p>
                    <p>Clique no link abaixo para redefinir sua senha:</p>
                    <a href="http://localhost:8000/usuario/validar-nova-senha/{token}">Redefinir Senha</a>
                    <br><br>
                    <p>Se você não solicitou essa alteração, ignore este e-mail.</p>
                    <br>
                    <p>Atenciosamente,<br>Equipe Esporte+</p>
                </body>
            </html>
        """
        return body


    def EmailConfirmacaoAgendamento(nome, agendamento):
        body = f"""
            <html lang="pt-BR">
                <head>
                    <meta charset="UTF-8">
                    <title>Agendamento Confirmado</title>
                </head>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <h2>Agendamento confirmado!</h2>
                    <p>Olá <strong>{nome}</strong>,</p>
                    <p>Seu agendamento foi realizado com sucesso.</p>
                    <p>Detalhes do agendamento:</p>
                    <ul>
                        <li><strong>Quadra:</strong> {agendamento.nome_quadra}</li>
                        <li><strong>Data:</strong> {agendamento.data}</li>
                        <li><strong>Horário de Início:</strong> {agendamento.horario_inicio}</li>
                        <li><strong>Horário de Fim:</strong> {agendamento.horario_fim}</li>
                    </ul>
                    <br>
                    <p>Atenciosamente,<br>Equipe Esporte+</p>
                </body>
            </html>
        """
        return body
    
    def EmailCancelamentoAgendamento(nome, agendamento):
        body = f"""
            <html lang="pt-BR">
                <head>
                    <meta charset="UTF-8">
                    <title>Agendamento Cancelado</title>
                </head>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <h2>Agendamento cancelado!</h2>
                    <p>Olá <strong>{nome}</strong>,</p>
                    <p>Seu agendamento foi cancelado.</p>
                    <p>Detalhes do agendamento:</p>
                    <ul>
                        <li><strong>Quadra:</strong> {agendamento.nome_quadra}</li>
                        <li><strong>Data:</strong> {agendamento.data}</li>
                        <li><strong>Horário de Início:</strong> {agendamento.horario_inicio}</li>
                        <li><strong>Horário de Fim:</strong> {agendamento.horario_fim}</li>
                    </ul>
                    <br>
                    <p>Atenciosamente,<br>Equipe Esporte+</p>
                </body>
            </html>
        """
        return body