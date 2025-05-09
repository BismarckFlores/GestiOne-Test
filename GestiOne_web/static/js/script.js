// Modals
const addModal = document.getElementById("addModal");
const editModal = document.getElementById("editModal");
const restockModal = document.getElementById("restockModal");
const registerSaleModal = document.getElementById("registerSaleModal"); // NEW MODAL

// Filter Inventory Table
function filterInventoryTable() {
    const idFilter = document.getElementById("inventoryIdFilter").value.toLowerCase();
    const nameFilter = document.getElementById("inventoryNameFilter").value.toLowerCase();
    const priceMinFilter = parseFloat(document.getElementById("inventoryPriceMinFilter").value) || -Infinity;
    const priceMaxFilter = parseFloat(document.getElementById("inventoryPriceMaxFilter").value) || Infinity;
    const quantityMinFilter = parseInt(document.getElementById("inventoryQuantityMinFilter").value) || -Infinity;
    const quantityMaxFilter = parseInt(document.getElementById("inventoryQuantityMaxFilter").value) || Infinity;

    const table = document.querySelector("#inventory table tbody");
    const rows = table.querySelectorAll("tr");

    rows.forEach(row => {
        const id = row.cells[0].textContent.toLowerCase();
        const name = row.cells[1].textContent.toLowerCase();
        const price = parseFloat(row.cells[2].textContent);
        const quantity = parseInt(row.cells[3].textContent);

        const idMatch = id.includes(idFilter);
        const nameMatch = name.includes(nameFilter);
        const priceMatch = price >= priceMinFilter && price <= priceMaxFilter;
        const quantityMatch = quantity >= quantityMinFilter && quantity <= quantityMaxFilter;

        if (idMatch && nameMatch && priceMatch && quantityMatch) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}

// Filter Sales Table
function filterSalesTable() {
    const idFilter = document.getElementById("salesIdFilter").value.toLowerCase();
    const productFilter = document.getElementById("salesProductFilter").value.toLowerCase();
    const dateFilter = document.getElementById("salesDateFilter").value;

    const table = document.querySelector("#sales-history table tbody");
    const rows = table.querySelectorAll("tr");

    rows.forEach(row => {
        const id = row.cells[0].textContent.toLowerCase();
        const product = row.cells[2].textContent.toLowerCase();
        const date = row.cells[5].textContent; // YYYY-MM-DD HH:MM:SS

        const idMatch = id.includes(idFilter);
        const productMatch = product.includes(productFilter);
        let dateMatch = true;

        if (dateFilter) {
            const saleDate = date.split(" ")[0]; // Get only the date part
            dateMatch = saleDate === dateFilter;
        }

        if (idMatch && productMatch && dateMatch) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}

// Settings Toggle
const toggleSettingsButton = document.getElementById("toggleSettings");
const settingsOptionsDiv = document.getElementById("settingsOptions");

toggleSettingsButton.addEventListener("click", function() {
    if (settingsOptionsDiv.style.display === "none") {
        settingsOptionsDiv.style.display = "block";
        toggleSettingsButton.textContent = "Ocultar Ajustes"; // Change button text
    } else {
        settingsOptionsDiv.style.display = "none";
        toggleSettingsButton.textContent = "Mostrar Ajustes"; // Change button text back
    }
});

// Add Modal
function showAddModal() {
    addModal.style.display = "block";
}

function closeAddModal() {
    addModal.style.display = "none";
}

// Edit Modal
function showEditModal(id, name, price) {
    editModal.style.display = "block";
    document.getElementById("edit_id").value = id;
    document.getElementById("edit_name").value = name;
    document.getElementById("edit_price").value = price;
    document.getElementById("editForm").action = `/edit_product/${id}`;
}

function closeEditModal() {
    editModal.style.display = "none";
}

// Restock Modal
function showRestockModal(id, name) {
    restockModal.style.display = "block";
    document.getElementById("restock_id").value = id;
    document.getElementById("restockForm").action = `/restock_product/${id}`;
}

function closeRestockModal() {
    restockModal.style.display = "none";
}

// Register Sale Modal (NEW)
function showRegisterSaleModal() {
    registerSaleModal.style.display = "block";
}

function closeRegisterSaleModal() {
    registerSaleModal.style.display = "none";
}

// Delete Confirmation
function confirmDelete(id) {
    if (confirm("¿Estás seguro de que quieres eliminar este producto?")) {
        window.location.href = `/delete_product/${id}`;
    }
}

// Close Modals on Outside Click
window.onclick = function (event) {
    if (event.target == addModal) {
        addModal.style.display = "none";
    }
    if (event.target == editModal) {
        editModal.style.display = "none";
    }
    if (event.target == restockModal) {
        restockModal.style.display = "none";
    }
    if (event.target == registerSaleModal) {  // NEW MODAL
        registerSaleModal.style.display = "none";
    }
}