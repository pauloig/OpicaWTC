document.addEventListener('DOMContentLoaded', function () {
    const regularHoursInput = document.getElementById('regular_hours');
    const vacationHoursInput = document.getElementById('vacation_hours');
    const sickHoursInput = document.getElementById('sick_hours');
    const otherHoursInput = document.getElementById('other_hours');

    const inputs = [vacationHoursInput, sickHoursInput, otherHoursInput];

    inputs.forEach(input => {
        input.addEventListener('input', updateRegularHours);
        input.addEventListener('blur', handleNullValues); // Check for null values on blur
    });

    function handleNullValues(event) {
        if (event.target.value === '') {
            event.target.value = 0;  // Set to 0 if the input is null/empty
            updateRegularHours();
        }
    }

    function updateRegularHours(event) {
        let totalOtherHours = 0;

        inputs.forEach(input => {
            totalOtherHours += parseFloat(input.value) || 0;
        });

        let remainingHours = 8 - totalOtherHours;

        if (remainingHours < 0) {
            alert('The total hours exceed the limit of 8.');

            // Reset the current input to 0
            event.target.value = 0;

            // Recalculate total after resetting the current input
            totalOtherHours = 0;
            inputs.forEach(input => {
                totalOtherHours += parseFloat(input.value) || 0;
            });

            remainingHours = 8 - totalOtherHours;
        }

        regularHoursInput.value = remainingHours;
    }
});