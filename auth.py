"""Email OTP authentication using Resend."""

from __future__ import annotations

import hashlib
import os
import secrets
import time

import streamlit as st


def _get_resend_api_key() -> str:
    """Retrieve Resend API key from environment or Streamlit secrets."""
    key = os.environ.get("RESEND_API_KEY", "")
    if not key:
        try:
            key = st.secrets.get("RESEND_API_KEY", "")
        except FileNotFoundError:
            key = ""
    return key


def _get_from_email() -> str:
    """Retrieve sender email from environment or Streamlit secrets."""
    email = os.environ.get("OTP_FROM_EMAIL", "")
    if not email:
        try:
            email = st.secrets.get("OTP_FROM_EMAIL", "onboarding@resend.dev")
        except FileNotFoundError:
            email = "onboarding@resend.dev"
    return email


def _hash_code(code: str) -> str:
    """Hash an OTP code for secure storage in session state."""
    return hashlib.sha256(code.encode()).hexdigest()


def send_otp(email: str) -> bool:
    """Generate a 6-digit OTP, send via Resend, store hash in session state.

    Returns True if email was sent successfully.
    """
    import resend

    api_key = _get_resend_api_key()
    if not api_key:
        st.error("Resend API key not configured. Contact your administrator.")
        return False

    resend.api_key = api_key

    code = f"{secrets.randbelow(900000) + 100000}"

    try:
        resend.Emails.send({
            "from": f"Mercato Partners Research <{_get_from_email()}>",
            "to": [email],
            "subject": "Your verification code — Mercato Partners Research",
            "html": (
                f"<div style='font-family: Inter, sans-serif; max-width: 400px; margin: 0 auto;'>"
                f"<h2 style='color: #0A0A0A;'>Mercato Partners</h2>"
                f"<p>Your verification code is:</p>"
                f"<p style='font-size: 32px; font-weight: 700; letter-spacing: 4px; "
                f"color: #0A0A0A; background: #F0F4F8; padding: 16px; "
                f"border-radius: 8px; text-align: center;'>{code}</p>"
                f"<p style='color: #777;'>This code expires in 10 minutes.</p>"
                f"<p style='color: #999; font-size: 12px;'>Mercato Partners — Internal Use Only</p>"
                f"</div>"
            ),
        })
    except Exception as e:
        st.error(f"Failed to send verification email: {e}")
        return False

    st.session_state["otp_hash"] = _hash_code(code)
    st.session_state["otp_email"] = email
    st.session_state["otp_expires"] = time.time() + 600  # 10 minutes

    return True


def verify_otp(email: str, code: str) -> bool:
    """Verify the OTP code against stored hash. Marks session as authenticated on success."""
    stored_hash = st.session_state.get("otp_hash")
    stored_email = st.session_state.get("otp_email")
    expires = st.session_state.get("otp_expires", 0)

    if not stored_hash or not stored_email:
        return False

    if time.time() > expires:
        st.error("Verification code expired. Please request a new one.")
        _clear_otp_state()
        return False

    if email != stored_email:
        return False

    if _hash_code(code.strip()) != stored_hash:
        return False

    # Mark authenticated for 24 hours
    st.session_state["auth_email"] = email
    st.session_state["auth_expires"] = time.time() + 86400  # 24 hours
    _clear_otp_state()
    return True


def _clear_otp_state():
    """Remove temporary OTP fields from session state."""
    for key in ("otp_hash", "otp_email", "otp_expires"):
        st.session_state.pop(key, None)


def is_authenticated() -> bool:
    """Check if the current session has a valid authentication."""
    auth_email = st.session_state.get("auth_email")
    auth_expires = st.session_state.get("auth_expires", 0)

    if not auth_email:
        return False
    if time.time() > auth_expires:
        st.session_state.pop("auth_email", None)
        st.session_state.pop("auth_expires", None)
        return False
    return True


def get_auth_email() -> str | None:
    """Return the authenticated user's email, or None."""
    if is_authenticated():
        return st.session_state.get("auth_email")
    return None


def render_auth_gate() -> bool:
    """Render the email OTP authentication UI.

    Returns True if user is authenticated, False otherwise.
    Shows email input → send code → verify code flow.
    """
    if is_authenticated():
        return True

    resend_key = _get_resend_api_key()
    if not resend_key:
        st.warning("Authentication is not configured. Contact your administrator to set up email verification.")
        return False

    st.markdown(
        '<div style="background: #F0F4F8; padding: 1.5rem; border-radius: 8px; '
        'border-left: 4px solid #1ABC9C; margin: 1rem 0;">'
        '<strong style="color: #0A0A0A;">Verification Required</strong><br>'
        '<span style="color: #777;">Enter your email to receive a verification code and unlock research generation.</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Step 1: Email input
    if "otp_hash" not in st.session_state:
        email = st.text_input("Email address", placeholder="you@mercatopartners.com", key="auth_email_input")
        if st.button("Send Verification Code", type="primary"):
            if not email or "@" not in email:
                st.error("Please enter a valid email address.")
            else:
                with st.spinner("Sending verification code..."):
                    if send_otp(email):
                        st.success(f"Verification code sent to **{email}**. Check your inbox.")
                        st.rerun()
        return False

    # Step 2: Code verification
    email = st.session_state.get("otp_email", "")
    st.info(f"Verification code sent to **{email}**")
    code = st.text_input("Enter 6-digit code", max_chars=6, placeholder="123456", key="auth_code_input")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Verify", type="primary"):
            if verify_otp(email, code):
                st.success("Verified! You can now generate research.")
                st.rerun()
            else:
                st.error("Invalid code. Please try again.")
    with col2:
        if st.button("Resend Code"):
            _clear_otp_state()
            st.rerun()

    return False
