// تحديد الانماط التي سنضيفها الى عناصر نموذج تسجيل الدخول والاشتراك عندما نريد التبديل الى نموذج الاشتراك مثل تحريك الخلفية الزرقاء الى اليمين والنموذج الى اليسار
// من html 
const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});