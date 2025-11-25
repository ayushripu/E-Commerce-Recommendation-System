// Additional JavaScript functionality can be added here

document.addEventListener("DOMContentLoaded", function () {
  // Add any interactive functionality here
  console.log("E-Commerce Recommendation System loaded");
});

// API call example
function getRecommendations(userId, method = "hybrid") {
  fetch(`/api/recommend/${userId}?method=${method}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        console.log("Recommendations:", data.recommendations);
      } else {
        console.error("Error:", data.error);
      }
    });
}
