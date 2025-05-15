const input = document.getElementById("userInput");

// تمدد الـ textarea أثناء الكتابة
input.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 150) + 'px';
});

async function sendMessage(event) {
    event.preventDefault(); // منع إعادة تحميل الصفحة

    const message = input.value.trim();
    if (message === "") return;

    const boxMessage = document.querySelector(".box-message");

    // ➡️ إنشاء قالب رسالة المستخدم (send)
    const userDiv = document.createElement("div");
    userDiv.classList.add("send");

    const userLabel = document.createElement("p");
    userLabel.textContent = "";

    const userMessage = document.createElement("p");
    userMessage.classList.add("message");
    userMessage.textContent = message;

    userDiv.appendChild(userLabel);
    userDiv.appendChild(userMessage);

    boxMessage.appendChild(userDiv);

    // ➡️ إنشاء قالب رد البوت (reply) مع "جاري الكتابة..."
    const botDiv = document.createElement("div");
    botDiv.classList.add("reply");

    const botLabel = document.createElement("p");
    botLabel.textContent = "";

    const botMessage = document.createElement("p");
    botMessage.classList.add("message");
    botMessage.textContent = "Typing..."; // البداية تكون جاري الكتابة

    botDiv.appendChild(botLabel);
    botDiv.appendChild(botMessage);

    boxMessage.appendChild(botDiv);

    // ➡️ تمرير لآخر الرسائل
    boxMessage.scrollTop = boxMessage.scrollHeight;

    // ➡️ إرسال الرسالة إلى السيرفر
    const response = await fetch("/send_message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });

    const data = await response.json();

    // ➡️ بعد استلام الرد، انتظر ثواني ثم ابدأ الكتابة كلمة كلمة
    await new Promise(resolve => setTimeout(resolve, 1000)); // تأخير بسيط بعد "جاري الكتابة..."

    // ➡️ تصفير الرسالة قبل كتابة الكلمات
    botMessage.textContent = "";

    // ➡️ كتابة الرد كلمة كلمة
    const words = data.response.split(' ');
    let index = 0;

    function typeWord() {
        if (index < words.length) {
            botMessage.textContent += words[index] + ' ';
            index++;
            setTimeout(typeWord, 250); // تأخير بين كل كلمة وكلمة (250 ملي ثانية)
        } else {
            boxMessage.scrollTop = boxMessage.scrollHeight; // بعد الانتهاء، تمرير لآخر الرسائل
        }
    }

    typeWord();

    // ➡️ تفريغ Textarea بعد الإرسال
    input.value = '';
    input.style.height = '1.5em'; // رجع ارتفاع الـ textarea الطبيعي
}
