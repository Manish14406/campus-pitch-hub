console.log("Submit pitch page loaded!");

// Get elements
const emailInput = document.querySelector("#student-email");
const checkbtn = document.getElementById("check-email");
const resultPara = document.getElementById("result");

// On button click
checkbtn.addEventListener("click", function () {

    const emailValue = emailInput.value.trim();

    // Empty input validation
    if (emailValue === "") {
        resultPara.textContent = "Please enter your email.";
        resultPara.style.color = "red";
        return;
    }

    // Backend validation
    fetch(`/verify-email?email=${emailValue}`)
        .then(response => response.json())
        .then(data => {

            if (data.valid) {
                resultPara.textContent = "Verified REVA student!";
                resultPara.style.color = "green";

                // Redirect after success
                setTimeout(() => {
                    window.location.href = "/pitch-submit-form";
                }, 1500);

            } else {
                resultPara.textContent = "Email not found in REVA student database!";
                resultPara.style.color = "red";
            }

        })
        .catch(error => {
            console.error("Error:", error);
            resultPara.textContent = "Server error!";
            resultPara.style.color = "red";
        });
});
