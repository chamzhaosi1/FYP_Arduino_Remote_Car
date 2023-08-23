var newDeviceSRInput = document.getElementById('new_device')
var newDeviceLNInput = document.getElementById('label_name')

newDeviceSRInput.addEventListener('focus', function() {
    this.removeAttribute('placeholder');
});

newDeviceSRInput.addEventListener('blur', function() {
    if (this.value === '') {
        this.setAttribute('placeholder', "Serial number");
    }
});

newDeviceLNInput.addEventListener('focus', function() {
    this.removeAttribute('placeholder');
});

newDeviceLNInput.addEventListener('blur', function() {
    if (this.value === '') {
        this.setAttribute('placeholder', "Label Name");
    }
});