(function () {
  const tokenKey = "ecommerceAccessToken";
  const output = document.getElementById("api-output");
  const tokenStatus = document.getElementById("token-status");
  const clearTokenBtn = document.getElementById("clear-token-btn");

  const readToken = () => localStorage.getItem(tokenKey) || "";
  const writeToken = (value) => {
    localStorage.setItem(tokenKey, value);
    syncTokenStatus();
  };
  const clearToken = () => {
    localStorage.removeItem(tokenKey);
    syncTokenStatus();
    if (output) {
      output.textContent = "Token dihapus.";
    }
  };

  const syncTokenStatus = () => {
    if (!tokenStatus) return;
    const token = readToken();
    tokenStatus.textContent = token ? "Access token tersimpan" : "Belum login";
  };

  const showResult = (data) => {
    if (!output) return;
    output.textContent = typeof data === "string" ? data : JSON.stringify(data, null, 2);
  };

  const requestJson = async (url, options) => {
    const response = await fetch(url, options);
    const text = await response.text();
    let payload;
    try {
      payload = text ? JSON.parse(text) : {};
    } catch (error) {
      payload = { raw: text };
    }
    if (!response.ok) {
      throw { status: response.status, payload };
    }
    return payload;
  };

  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(loginForm);
      try {
        const data = await requestJson("/login/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: formData.get("username"),
            password: formData.get("password"),
          }),
        });
        writeToken(data.access);
        showResult(data);
      } catch (error) {
        showResult(error.payload || { error: "Login gagal" });
      }
    });
  }

  const checkoutForm = document.getElementById("checkout-form");
  if (checkoutForm) {
    checkoutForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const token = readToken();
      if (!token) {
        showResult({ error: "Login dulu untuk checkout." });
        return;
      }
      const formData = new FormData(checkoutForm);
      try {
        const data = await requestJson("/checkout/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            product_id: formData.get("product_id"),
            quantity: formData.get("quantity"),
          }),
        });
        showResult(data);
      } catch (error) {
        showResult(error.payload || { error: "Checkout gagal" });
      }
    });
  }

  const orderForm = document.getElementById("order-form");
  if (orderForm) {
    orderForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const token = readToken();
      if (!token) {
        showResult({ error: "Login dulu untuk lihat order." });
        return;
      }
      const formData = new FormData(orderForm);
      try {
        const data = await requestJson(`/order/${formData.get("order_id")}/`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        showResult(data);
      } catch (error) {
        showResult(error.payload || { error: "Order tidak ditemukan" });
      }
    });
  }

  if (clearTokenBtn) {
    clearTokenBtn.addEventListener("click", clearToken);
  }

  syncTokenStatus();
})();
