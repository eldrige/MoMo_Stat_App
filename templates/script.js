document.addEventListener("DOMContentLoaded", () => {
    fetch("http://127.0.0.1:5000/transactions")
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById("transaction-table");

            data.forEach(transaction => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${transaction.date}</td>
                    <td>${transaction.time}</td>
                    <td>${transaction.new_balance}</td>
                    <td>${transaction.transaction_id}</td>
                    <td>${transaction.amount}</td>
                `;

                table.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching transactions:", error));
});
