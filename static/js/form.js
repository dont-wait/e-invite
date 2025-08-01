const fileInput = document.querySelector('input[type="file"]');
const previewSection = document.getElementById("excel-preview");
const tbody = previewSection.querySelector("tbody");

fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (e) {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });
        const sheet = workbook.Sheets[workbook.SheetNames[0]];
        const json = XLSX.utils.sheet_to_json(sheet);

        tbody.innerHTML = ""; // Xóa bảng cũ

        json.forEach(row => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                    <td>${row["STT"] || ""}</td>
                    <td>${row["Họ Tên PH"] || ""}</td>
                    <td>${row["Giới Tính"] || ""}</td>
                    <td>${row["Họ Tên Học Sinh"] || ""}</td>
                `;
            tbody.appendChild(tr);
        });

        // Hiện phần bảng nếu đọc thành công
        if (json.length > 0) {
            previewSection.style.display = "block";
        }
    };
    reader.readAsArrayBuffer(file);
});
