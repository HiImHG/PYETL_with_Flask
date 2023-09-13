function toggleChildOptions(area) {
    var checkboxContainer = document.getElementById(area);
    checkboxContainer.style.display = 'block';

    updateParentOptions(area);
}

function updateParentOptions(area) {
    var parentCategory = area.split('_')[0];
    var parentCheckbox = document.getElementById(parentCategory + 'Checkbox');
    var checkboxContainer = document.getElementById(area);
    var checkboxes = checkboxContainer.querySelectorAll('input[type="checkbox"]');

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            parentCheckbox.checked = true;
            return;
        }
    }

    parentCheckbox.checked = false;
    checkboxContainer.style.display = 'none';
}

function updateParentCheckbox(area) {
    var parentCheckbox = document.getElementById(area + 'Checkbox');
    var checkboxContainer = document.getElementById(area);
    var checkboxes = checkboxContainer.querySelectorAll('input[type="checkbox"]');

    var allChecked = true;
    var someChecked = false;

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            someChecked = true;
        } else {
            allChecked = false;
        }
    }

    if (allChecked) {
        parentCheckbox.checked = true;
        parentCheckbox.indeterminate = false;
    } else if (someChecked) {
        parentCheckbox.checked = false;
        parentCheckbox.indeterminate = true;
    } else {
        parentCheckbox.checked = false;
        parentCheckbox.indeterminate = false;
    }
}
const checkboxes = document.querySelectorAll('#category-wrapper input[type="checkbox"]');

const selectedAreasList = document.getElementById('selectedAreas');

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('click', () => {
        selectedAreasList.innerHTML = '';

        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                const listItem = document.createElement('li');
                listItem.textContent = checkbox.value;

                selectedAreasList.appendChild(listItem);
            }
        });
    });
});

function uncheckAll() {
    const checkboxes = document.querySelectorAll('#category-wrapper input[type="checkbox"]');

    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });

    updateSelectedAreasList();
}

function updateSelectedAreasList() {
    const checkboxes = document.querySelectorAll('#category-wrapper input[type="checkbox"]');
    const selectedAreasList = document.getElementById('selectedAreas');

    selectedAreasList.innerHTML = '';

    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            const listItem = document.createElement('li');
            listItem.textContent = checkbox.value;

            selectedAreasList.appendChild(listItem);
        }
    });
}