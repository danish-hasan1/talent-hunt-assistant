document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('signinForm');
  const emailInput = document.getElementById('emailInput');

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = emailInput.value.trim();
    if (email) {
      // In a real app we might store this in localStorage so the Streamlit app can read it,
      // or we can simply pass it as a URL parameter if Streamlit handles that.
      // We will redirect to Streamlit app
      window.location.href = `http://localhost:8511/?email=${encodeURIComponent(email)}`;
    }
  });

  // Simple parallax effect for orbs
  document.addEventListener('mousemove', (e) => {
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    
    const orbs = document.querySelectorAll('.orb');
    orbs.forEach((orb, index) => {
      const speed = (index + 1) * 20;
      orb.style.transform = `translate(${x * speed}px, ${y * speed}px)`;
    });
  });
});
