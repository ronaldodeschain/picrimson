from fastapi import Request
import os
import smtplib
import json
from email.message import EmailMessage


def _get_cart(request: Request) -> list[dict]:
    return request.session.get("cart", [])


def _save_cart(request: Request, cart: list[dict]) -> None:
    request.session["cart"] = cart


def _cart_total(cart: list[dict]) -> float:
    return sum(item.get("valor", 0.0) * item.get("quantidade", 1) for item in cart)


def _format_cart_item(produto, tamanho: str, material: str, pintura: str) -> dict:
    return {
        "produto_id": produto.id_produto,
        "nome": produto.nome_produto,
        "valor": float(produto.valor or 0.0),
        "tamanho": tamanho,
        "material": material,
        "pintura": pintura,
        "quantidade": 1,
        "link": f"/produto/{produto.id_produto}",
        "categoria": produto.id_categoria,
        "imagem": produto.imagens[0].arquivo_imagem if produto.imagens and len(produto.imagens) > 0 else None,
    }


def _find_cart_item(cart: list[dict], produto_id: int, tamanho: str, material: str, pintura: str):
    for index, item in enumerate(cart):
        if item["produto_id"] == produto_id and item["tamanho"] == tamanho and item["material"] == material and item["pintura"] == pintura:
            return index, item
    return None, None


def _send_email(subject: str, body: str, to_address: str) -> bool:
    smtp_host = os.getenv("EMAIL_SMTP_HOST")
    smtp_port_raw = os.getenv("EMAIL_SMTP_PORT", "587")
    try:
        smtp_port = int(smtp_port_raw)
    except (TypeError, ValueError):
        smtp_port = 587
    smtp_user = os.getenv("EMAIL_SMTP_USER")
    smtp_password = os.getenv("EMAIL_SMTP_PASSWORD")
    from_address = os.getenv("EMAIL_FROM", smtp_user or "no-reply@crimsonclaw.local")
    if not smtp_host or not smtp_user or not smtp_password:
        # Log to console in development and return False so caller can persist locally
        print("[cart] SMTP configuration missing, email not sent.")
        print(subject)
        print(body)
        return False
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_address
        msg["To"] = to_address
        msg.set_content(body)
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        return True
    except Exception as exc:
        print(f"[cart] Failed to send email: {exc}")
        return False
