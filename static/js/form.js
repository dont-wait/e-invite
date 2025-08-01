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

document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.querySelector('input[type="file"]');
    const previewSection = document.getElementById("excel-preview");
    const previewBody = previewSection.querySelector("tbody");
    const submitBtn = document.querySelector(".submit-btn");

    let parsedExcelData = [];

    fileInput.addEventListener("change", function (e) {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function (e) {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, { type: "array" });
            const sheet = workbook.Sheets[workbook.SheetNames[0]];
            const rows = XLSX.utils.sheet_to_json(sheet, { header: 1 });

            // Skip header
            parsedExcelData = [];
            previewBody.innerHTML = "";

            for (let i = 1; i < rows.length; i++) {
                const [stt, parent_name, gender, student_name] = rows[i];
                if (!parent_name || !student_name) continue;

                parsedExcelData.push({ parent_name, gender, student_name });

                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${stt || i}</td>
                    <td>${parent_name}</td>
                    <td>${gender}</td>
                    <td>${student_name}</td>
                `;
                previewBody.appendChild(tr);
            }

            previewSection.style.display = "block";
        };
        reader.readAsArrayBuffer(file);
    });

    submitBtn.addEventListener("click", async function (e) {
        e.preventDefault();

        if (parsedExcelData.length === 0) {
            alert("Vui lòng chọn file Excel hợp lệ!");
            return;
        }

        // Lấy các giá trị chung từ form
        const getValue = id => document.getElementById(id)?.value || "";
        const shared = {
            class: getValue("class"),
            school_name: getValue("school_name"),
            city_department_of_education: getValue("city_department_of_education"),
            address: getValue("address"),
            city: getValue("city"),
            purpose: getValue("purpose"),
            date_meeting: getValue("date_meeting"),
            date_write: getValue("date_write"),
            teacher: getValue("teacher")
        };

        // Gộp với từng dòng Excel
        const infos = parsedExcelData.map(row => ({
            ...shared,
            parent_name: row.parent_name,
            gender: row.gender,
            student_name: row.student_name
        }));

        const payload = { infos };

        try {
            const res = await fetch("/generate-invites", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const result = await res.json();
            if (res.ok) {
                alert(result.message);
            } else {
                alert("❌ Lỗi: " + result.message);
            }
        } catch (err) {
            alert("Không thể gửi dữ liệu: " + err.message);
        }
    });
});
