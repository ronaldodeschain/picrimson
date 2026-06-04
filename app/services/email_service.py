import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


class EmailService:
    """Serviço para enviar emails via SMTP."""

    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER") or os.getenv("EMAIL_SMTP_HOST", "smtp.gmail.com")
        port_value = os.getenv("SMTP_PORT") or os.getenv("EMAIL_SMTP_PORT", "587")
        try:
            self.smtp_port = int(port_value)
        except (TypeError, ValueError):
            self.smtp_port = 587
        self.sender_email = os.getenv("SENDER_EMAIL") or os.getenv("EMAIL_SMTP_USER")
        self.sender_password = os.getenv("SENDER_PASSWORD") or os.getenv("EMAIL_SMTP_PASSWORD")

    async def enviar_email(
        self, 
        destinatario: str, 
        assunto: str, 
        corpo_html: str,
        corpo_texto: str | None = None
    ) -> bool:
        """
        Envia um email via SMTP.
        
        Args:
            destinatario: Email do destinatário
            assunto: Assunto do email
            corpo_html: Corpo do email em HTML
            corpo_texto: Corpo do email em texto (opcional)
        
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        try:
            if not self.sender_email or not self.sender_password:
                print("SMTP credentials not configured")
                return False

            # Criar mensagem
            mensagem = MIMEMultipart("alternative")
            mensagem["Subject"] = assunto
            mensagem["From"] = self.sender_email
            mensagem["To"] = destinatario

            # Adicionar versão em texto simples (fallback)
            if corpo_texto:
                part1 = MIMEText(corpo_texto, "plain")
                mensagem.attach(part1)
            
            # Adicionar versão em HTML (preferida)
            part2 = MIMEText(corpo_html, "html")
            mensagem.attach(part2)

            # Conectar ao servidor SMTP e enviar
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, destinatario, mensagem.as_string())

            print(f"Email enviado com sucesso para {destinatario}")
            return True

        except smtplib.SMTPAuthenticationError:
            print("Erro de autenticação SMTP: verifique email e senha")
            return False
        except smtplib.SMTPException as e:
            print(f"Erro ao enviar email: {e}")
            return False
        except Exception as e:
            print(f"Erro inesperado ao enviar email: {e}")
            return False
