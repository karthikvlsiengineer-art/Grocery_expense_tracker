const API = "https://grocery-expense-tracker.onrender.com";

document.addEventListener("DOMContentLoaded", function () {

const form = document.getElementById("expenseForm");

form.addEventListener("submit", function(e){

e.preventDefault();

let item = document.getElementById("item").value;
let amount = document.getElementById("amount").value;
let date = document.getElementById("date").value;

fetch(API + "/add-expense",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
item:item,
amount:amount,
date:date
})
})
.then(res => res.json())
.then(data => {

form.reset();
loadExpenses();
loadCharts();

})
.catch(err => console.log(err));

});

loadExpenses();
loadCharts();

});

function loadExpenses(){

fetch(API + "/expenses")
.then(res => res.json())
.then(data => {

let table = document.getElementById("expenseTable");
table.innerHTML = "";

let total = 0;

data.forEach(e => {

total += e.amount;

table.innerHTML += `
<tr>
<td>${e.item}</td>
<td>₹${e.amount}</td>
<td>${e.date}</td>
<td>
<button onclick="deleteExpense(${e.id})">Delete</button>
</td>
</tr>
`;

});

document.getElementById("totalExpense").innerText = total;

});

}

function deleteExpense(id){

fetch(API + "/delete/" + id,{
method:"DELETE"
})
.then(()=>loadExpenses());

}

function loadCharts(){

fetch(API + "/chart-data")
.then(res => res.json())
.then(data => {

new Chart(
document.getElementById("pieChart"),
{
type:'pie',
data:{
labels:data.item_labels,
datasets:[{
data:data.item_values
}]
}
});

new Chart(
document.getElementById("barChart"),
{
type:'bar',
data:{
labels:data.month_labels,
datasets:[{
label:'Monthly Expense',
data:data.month_values
}]
}
});

});

}