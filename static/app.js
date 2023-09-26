function validateForm() {
    var creditScoreInput = document.getElementById("credit_score");
    var age = document.getElementById("age");
    var tenure = document.getElementById("tenure");
    var balance = document.getElementById("balance");
    var prods = document.getElementById("prods");
    var sal = document.getElementById("sal");

    // Validate Credit Score (Example)
    if (parseInt(creditScoreInput.value) < 300 || parseInt(creditScoreInput.value) > 850) {
        alert("Credit Score must be between 300 and 850.");
        return false; 
    }

    if (parseInt(age.value) < 18 || parseInt(age.value) > 100) {
        alert("Age must be between 18 and 100.");
        return false; 
    }

    if (parseInt(tenure.value) < 0 || parseInt(tenure.value) > 10) {
        alert("Tenure must be between 0 and 10.");
        return false; 
    }

    if (parseInt(balance.value) < 0) {
        alert("Balance should be a non-negative integer.");
        return false; 
    }

    if (parseInt(prods.value) < 0 || parseInt(prods.value) > 5) {
        alert("Number of products used by the customer must be between 0 and 5.");
        return false;
    }

    if (parseInt(sal.value) < 0) {
        alert("Salary should be a non-negative integer.");
        return false; 
    }

    return true; // If all validations pass, allow form submission
}
