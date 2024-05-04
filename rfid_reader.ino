<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel</title>
</head>
<body>
    <h1>Admin Panel</h1>

    <!-- Existing form for adding keys -->
    <h2>Pievienot Atslegu</h2>
    <form action="/add_key" method="POST">
        <!-- Existing input fields -->
        <input type="submit" value="Pievienot Atslegu">
    </form>

    <!-- Add button for RFID scanning -->
    <button onclick="scanRFID()">Scan RFID</button>

    <!-- Existing employee and key lists -->
</body>
</html>

<script>
function scanRFID() {
    fetch('/add_key_rfid', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        // Handle success, if needed
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
</script>
