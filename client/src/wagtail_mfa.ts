import "./styles/index.scss";

// Handle navigation to the edit page after registering
document.addEventListener("otp_webauthn.register_complete", ((
  event: CustomEvent,
) => {
  const id = event.detail.id;
  const deviceInput =
    document.querySelector<HTMLInputElement>("input[name=device]");
  deviceInput!.value = id;
  deviceInput!.form!.submit();
}) as EventListener);
