// Build Sheet Generator V3 - Frontend JavaScript

// Global state
let selectedCPU = null;
let currentPrice = 0;

// DOM Elements
const form = document.getElementById('buildsheet-form');
const computerTypeSelect = document.getElementById('computer_type');
const laptopSection = document.getElementById('laptop_section');
const cpuEntryMode = document.getElementById('cpu_entry_mode');
const cpuSearchMode = document.getElementById('cpu_search_mode');
const cpuManualMode = document.getElementById('cpu_manual_mode');
const cpuSearchInput = document.getElementById('cpu_search');
const cpuSuggestions = document.getElementById('cpu_suggestions');
const cpuSelectedInfo = document.getElementById('cpu_selected_info');
const cpuInfoText = document.getElementById('cpu_info_text');
const drivesContainer = document.getElementById('drives_container');
const addDriveBtn = document.getElementById('add_drive_btn');
const recalculateBtn = document.getElementById('recalculate_btn');
const errorMessage = document.getElementById('error_message');

// Event Listeners
document.addEventListener('DOMContentLoaded', init);

function init() {
    // Computer type change
    computerTypeSelect.addEventListener('change', handleComputerTypeChange);

    // CPU entry mode
    cpuEntryMode.addEventListener('change', handleCPUEntryModeChange);

    // CPU search
    cpuSearchInput.addEventListener('input', debounce(handleCPUSearch, 300));

    // Price calculation
    recalculateBtn.addEventListener('click', calculatePrice);

    // Form submission
    form.addEventListener('submit', handleFormSubmit);
}

function handleComputerTypeChange() {
    const isLaptop = computerTypeSelect.value === 'laptop';
    laptopSection.style.display = isLaptop ? 'block' : 'none';
}

function handleCPUEntryModeChange() {
    const mode = cpuEntryMode.value;
    if (mode === 'search') {
        cpuSearchMode.style.display = 'block';
        cpuManualMode.style.display = 'none';
    } else {
        cpuSearchMode.style.display = 'none';
        cpuManualMode.style.display = 'block';
        selectedCPU = null;
        cpuSelectedInfo.style.display = 'none';
    }
}

async function handleCPUSearch(e) {
    const query = e.target.value.trim();

    if (query.length < 2) {
        cpuSuggestions.classList.remove('active');
        cpuSuggestions.innerHTML = '';
        return;
    }

    try {
        const response = await fetch(`/api/search_cpu?q=${encodeURIComponent(query)}`);
        const cpus = await response.json();

        if (cpus.length > 0) {
            displayCPUSuggestions(cpus);
        } else {
            cpuSuggestions.innerHTML = '<div class="suggestion-item"><small>No CPUs found. Try a different search or use Manual Entry.</small></div>';
            cpuSuggestions.classList.add('active');
        }
    } catch (error) {
        console.error('CPU search error:', error);
        showError('Failed to search CPUs. Please try manual entry.');
    }
}

function displayCPUSuggestions(cpus) {
    cpuSuggestions.innerHTML = '';

    cpus.forEach(cpu => {
        const div = document.createElement('div');
        div.className = 'suggestion-item';
        div.innerHTML = `
            <strong>${cpu.name}</strong>
            <small>Year: ${cpu.year} | Cores: ${cpu.cores} | Threads: ${cpu.threads} | Passmark: ${cpu.passmark}</small>
        `;
        div.addEventListener('click', () => selectCPU(cpu));
        cpuSuggestions.appendChild(div);
    });

    cpuSuggestions.classList.add('active');
}

function selectCPU(cpu) {
    selectedCPU = cpu;
    cpuSearchInput.value = cpu.name;
    cpuSuggestions.classList.remove('active');

    // Display selected CPU info
    cpuInfoText.innerHTML = `
        <strong>${cpu.name}</strong><br>
        Year: ${cpu.year} | Cores: ${cpu.cores} | Threads: ${cpu.threads} | Base: ${cpu.clock} MHz | Turbo: ${cpu.turbo} MHz | Passmark: ${cpu.passmark}
    `;
    cpuSelectedInfo.style.display = 'block';

    // Auto-calculate price
    calculatePrice();
}

function addDriveEntry() {
    const driveEntry = document.createElement('div');
    driveEntry.className = 'drive-entry form-grid';
    driveEntry.innerHTML = `
        <div class="form-group">
            <label>Capacity (GB) <span class="required">*</span></label>
            <input type="number" class="drive_capacity" required min="1" placeholder="e.g., 512">
        </div>
        <div class="form-group">
            <label>Type <span class="required">*</span></label>
            <select class="drive_type" required>
                <option value="HDD">HDD</option>
                <option value="SSD" selected>SSD</option>
                <option value="NVMe">NVMe SSD</option>
            </select>
        </div>
        <div class="form-group">
            <button type="button" class="btn-remove-drive">Remove</button>
        </div>
    `;
    drivesContainer.appendChild(driveEntry);
    setupDriveRemoveButtons();
}

function setupDriveRemoveButtons() {
    const removeButtons = document.querySelectorAll('.btn-remove-drive');
    removeButtons.forEach((btn, index) => {
        // First drive button should be hidden
        if (index === 0) {
            btn.style.visibility = 'hidden';
        } else {
            btn.style.visibility = 'visible';
            btn.onclick = function () {
                this.closest('.drive-entry').remove();
            };
        }
    });
}

async function calculatePrice() {
    const priceLoading = document.getElementById('price_loading');
    const priceResult = document.getElementById('price_result');
    const priceBreakdown = document.getElementById('price_breakdown');

    priceLoading.style.display = 'block';
    priceResult.style.display = 'none';
    priceBreakdown.style.display = 'none';

    try {
        const data = collectFormData();

        const response = await fetch('/api/calculate_price', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            displayPrice(result);
        } else {
            throw new Error(result.error || 'Price calculation failed');
        }
    } catch (error) {
        console.error('Price calculation error:', error);
        showError('Failed to calculate price: ' + error.message);
    } finally {
        priceLoading.style.display = 'none';
        priceResult.style.display = 'block';
    }
}

function displayPrice(result) {
    currentPrice = result.final_price;

    document.getElementById('final_price').textContent = result.final_price;
    document.getElementById('price_cpu').textContent = result.breakdown.cpu_price;
    document.getElementById('price_ram').textContent = result.breakdown.ram_price;
    document.getElementById('price_drive').textContent = result.breakdown.drive_price;
    document.getElementById('price_gpu').textContent = result.breakdown.gpu_price;
    document.getElementById('price_os').textContent = result.breakdown.os_modifier;
    document.getElementById('price_base').textContent = result.breakdown.base_fee;
    document.getElementById('price_total').textContent = result.final_price;

    document.getElementById('price_breakdown').style.display = 'block';
}

function collectFormData() {
    const mode = cpuEntryMode.value;
    const data = {
        is_laptop: computerTypeSelect.value === 'laptop',
        ram_gb: document.getElementById('ram_gb').value,
        ram_type: document.getElementById('ram_type').value,
        gpu_price: document.getElementById('gpu_price').value || 0,
        gpu_price: document.getElementById('gpu_price').value || 0,
        os_price_type: document.getElementById('os_price_type').value,
        os_name: document.getElementById('os_name').value,
        drives: []
    };

    // Collect drives
    const driveCapacities = document.querySelectorAll('.drive_capacity');
    const driveTypes = document.querySelectorAll('.drive_type');

    driveCapacities.forEach((input, index) => {
        if (input.value) {
            data.drives.push({
                capacity: parseFloat(input.value),
                type: driveTypes[index].value
            });
        }
    });

    // CPU data
    if (mode === 'search' && selectedCPU) {
        data.cpu_name = selectedCPU.name;
        data.cpu_model_name = selectedCPU.name;
    } else if (mode === 'manual') {
        data.cpu_name = document.getElementById('cpu_name_manual').value;
        data.manual_passmark = document.getElementById('cpu_passmark').value;
        // These are not used in pricing but needed for PDF
        data.cpu_year = document.getElementById('cpu_year').value;
        data.cpu_cores = document.getElementById('cpu_cores').value;
        data.cpu_threads = document.getElementById('cpu_threads').value;
        data.cpu_turbo = document.getElementById('cpu_turbo').value;
    }

    return data;
}

async function handleFormSubmit(e) {
    e.preventDefault();

    const generateBtn = document.getElementById('generate_btn');
    const originalText = generateBtn.textContent;
    generateBtn.textContent = 'Generating PDF...';
    generateBtn.disabled = true;

    try {
        const formData = collectFullFormData();

        const response = await fetch('/api/generate_buildsheet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            // Download the PDF
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `BuildSheet_${formData.model.replace(/\s+/g, '_')}_${formData.serial}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            showSuccess('Build sheet generated successfully!');
        } else {
            const error = await response.json();
            throw new Error(error.error || 'Failed to generate build sheet');
        }
    } catch (error) {
        console.error('Form submission error:', error);
        showError('Failed to generate build sheet: ' + error.message);
    } finally {
        generateBtn.textContent = originalText;
        generateBtn.disabled = false;
    }
}

function collectFullFormData() {
    const mode = cpuEntryMode.value;
    const data = {
        model: document.getElementById('model').value,
        serial: document.getElementById('serial').value,
        builder_name: document.getElementById('builder_name').value,
        is_laptop: computerTypeSelect.value === 'laptop',
        ram_gb: document.getElementById('ram_gb').value,
        ram_type: document.getElementById('ram_type').value,
        gpu_name: document.getElementById('gpu_name').value,
        gpu_price: document.getElementById('gpu_price').value || 0,
        gpu_price: document.getElementById('gpu_price').value || 0,
        os_price_type: document.getElementById('os_price_type').value,
        os_name: document.getElementById('os_name').value,
        wifi: document.getElementById('wifi').checked,
        bluetooth: document.getElementById('bluetooth').checked,
        webcam: document.getElementById('webcam').checked,
        touchscreen: document.getElementById('touchscreen').checked,
        sound: document.getElementById('sound').checked,
        microphone: document.getElementById('microphone').checked,
        price: document.getElementById('actual_price').value,  // User-entered actual price
        drives: []
    };

    // Collect drives
    const driveCapacities = document.querySelectorAll('.drive_capacity');
    const driveTypes = document.querySelectorAll('.drive_type');

    driveCapacities.forEach((input, index) => {
        if (input.value) {
            data.drives.push({
                capacity: parseFloat(input.value),
                type: driveTypes[index].value
            });
        }
    });

    // CPU data
    if (mode === 'search' && selectedCPU) {
        data.cpu_name = selectedCPU.name;
        data.cpu_model_name = selectedCPU.name;
        data.cpu_cores = selectedCPU.cores;
        data.cpu_threads = selectedCPU.threads;
        // DB stores clock/turbo in GHz already — no /1000 conversion needed
        data.cpu_turbo = parseFloat(selectedCPU.turbo).toFixed(2);
        // Use base clock for PDF display; fall back to turbo if clock is 0/missing in DB
        const baseClock = selectedCPU.clock && selectedCPU.clock > 0
            ? parseFloat(selectedCPU.clock).toFixed(2)
            : parseFloat(selectedCPU.turbo).toFixed(2);
        data.cpu_speed = baseClock;
    } else if (mode === 'manual') {
        data.cpu_name = document.getElementById('cpu_name_manual').value;
        data.cpu_cores = document.getElementById('cpu_cores').value;
        data.cpu_threads = document.getElementById('cpu_threads').value;
        data.cpu_turbo = document.getElementById('cpu_turbo').value;
        // Use base clock for PDF display; fall back to turbo if base clock field is left blank
        const baseClockManual = document.getElementById('cpu_base_clock').value;
        data.cpu_speed = baseClockManual || data.cpu_turbo;
        data.manual_passmark = document.getElementById('cpu_passmark').value;
    }

    // Laptop-specific
    if (data.is_laptop) {
        data.screen_size = document.getElementById('screen_size').value;
        data.battery_health = document.getElementById('battery_health').value;
        data.battery_duration = document.getElementById('battery_duration').value;
    }

    return data;
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

function showSuccess(message) {
    // Create a success message element
    const successDiv = document.createElement('div');
    successDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #10b981;
        color: white;
        padding: 1rem 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    successDiv.textContent = message;
    document.body.appendChild(successDiv);

    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

// Utility: Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Close suggestions when clicking outside
document.addEventListener('click', (e) => {
    if (!cpuSearchInput.contains(e.target) && !cpuSuggestions.contains(e.target)) {
        cpuSuggestions.classList.remove('active');
    }
});
