import logging
import smtplib
import ssl
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from project.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS, DEBUG

logger = logging.getLogger('django')

def sendmail(from_email, destinatarios, subject, html_body):

	host = str(EMAIL_HOST)
	port = int(EMAIL_PORT)
	user = str(EMAIL_HOST_USER)
	password = str(EMAIL_HOST_PASSWORD)

	try:
		# Crear contexto SSL que no verifica certificados
		if not DEBUG:
			context = ssl.create_default_context()
			context.check_hostname = False
			context.verify_mode = ssl.CERT_NONE

		# Conectar al servidor SMTP
		if not DEBUG:
			server = smtplib.SMTP(host, port)
			if EMAIL_USE_TLS:
				server.starttls(context=context)
			server.login(user, password)

		# Crear mensaje MIME
		msg = MIMEText(html_body, "html", "utf-8")
		msg["From"] = formataddr((str(Header("Alarmas", "utf-8")), from_email))
		msg["To"] = ", ".join(destinatarios)
		msg["Subject"] = subject

		# Enviar correo
		if not DEBUG:
			server.sendmail(from_email, destinatarios, msg.as_string())
			server.quit()
			return True, "Correo enviado exitosamente."
		else:
			logger.info(f"DEBUG MODE: Simulando envío de email a {destinatarios} con subject '{subject}'")
			return True, "DEBUG MODE: Simulando envío de email."
	except Exception as e:
		logger.error(f"Error enviando email: {e}")
		return False, str(e)


def send_bulk_mails(mails):
	"""
	Envía varios correos reutilizando una sola conexión SMTP.
	Retorna un resultado individual para cada correo, siempre.

	Args:
		mails (list of dict): cada dict debe tener:
			- id (str)
			- from_email (str)
			- destinatarios (list[str])
			- subject (str)
			- html_body (str)

	Returns:
		list of dict: con el estado de cada envío
	"""
	results = []
	host = str(EMAIL_HOST)
	port = int(EMAIL_PORT)
	user = str(EMAIL_HOST_USER)
	password = str(EMAIL_HOST_PASSWORD)

	try:
		# Configuración SSL (ignora verificación)
		if not DEBUG:
			context = ssl.create_default_context()
			context.check_hostname = False
			context.verify_mode = ssl.CERT_NONE

		# Conectar al servidor SMTP
		if not DEBUG:
			server = smtplib.SMTP(host, port)
			if EMAIL_USE_TLS:
				server.starttls(context=context)
			server.login(user, password)

		# Recorrer cada correo
		for mail in mails:
			try:
				from_email = str(mail["from_email"])
				destinatarios = [str(d) for d in mail["destinatarios"]]
				subject = str(mail["subject"])
				html_body = str(mail["html_body"])

				msg = MIMEText(html_body, "html", "utf-8")
				msg["From"] = from_email
				msg["To"] = ", ".join(destinatarios)
				msg["Subject"] = subject

				if not DEBUG:
					server.send_message(msg, from_addr=from_email, to_addrs=destinatarios)

				result = {
					"id": mail["id"],
					"to": destinatarios,
					"subject": subject,
					"status": True,
				}
				if DEBUG:
					result["status_real"] = "DEBUG MODE: Simulando envío de email."
				result["error"] = None
				results.append(result)
				logger.info(f"DEBUG MODE: Simulando envío de email a {destinatarios} con subject '{subject}'")
			except Exception as e:
				# Captura fallo individual y continúa con los demás
				results.append({
					"id": mail["id"],
					"to": mail.get("destinatarios"),
					"subject": mail.get("subject"),
					"status": False,
					"error": str(e)
				})

		if not DEBUG:
			server.quit()

	except Exception as e:
		# Si falla toda la conexión SMTP, todos los correos devuelven error
		for mail in mails:
			results.append({
				"id": mail["id"],
				"to": mail.get("destinatarios"),
				"subject": mail.get("subject"),
				"status": False,
				"error": f"Error global SMTP: {e}"
			})

	return results
