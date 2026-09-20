const links = document.querySelectorAll(".navbar a");


for (const link of links) {
    link.addEventListener("click",  function(e) {
        e.preventDefault();
        const hrefAttribute = link.getAttribute("href");
        const sectionElement = document.querySelector(hrefAttribute);
        sectionElement.scrollIntoView({ behavior: "smooth", block: "start" })

    } )
}

function handleIntersection(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add("visible");
        }
        else {
            entry.target.classList.remove("visible");
        }
            
        
    });
}

const allsections = document.querySelectorAll("section");
const observer = new IntersectionObserver(handleIntersection);

for (const section of allsections) {
    observer.observe(section);
}

const canvas = document.getElementById("starfield");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const stars = [];


for (let i = 0; i < 200; i++) {
    let randomX = Math.random() * canvas.width;
    let randomY = Math.random() * canvas.height;
    let min = 1;
    let max = 2.5;
    let radius = Math.random() * (max - min) + min;
    let dx = Math.random() * (0.1 - -0.1) + -0.1;
    let dy = Math.random() * (0.1 - -0.1) + -0.1;
    stars.push({ x: randomX, y: randomY, radius: radius, dx:dx, dy:dy });
}

ctx.fillStyle = "#FFF"

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    for (const star of stars) {
        star.x += star.dx
        star.y += star.dy
        if (star.x > canvas.width) { star.x = 0; }
        if (star.x < 0) { star.x = canvas.width; }
        if (star.y > canvas.height) { star.y = 0; }
        if (star.y < 0) { star.y = canvas.height; }
        
        ctx.beginPath();
        ctx.arc(star.x, star.y , star.radius, 0, Math.PI * 2);
        ctx.fill();

    }

    requestAnimationFrame(animate);
}


const chartCanvas = document.getElementById("interactiveTable");
new Chart(chartCanvas, {
    type: "bar",
    data: {
        labels: ["Barnes-Hut pure Python","O(N²) pure Python", "NumPy vectorized"],
        datasets: [{
            label: "Time (s)",
            data: [100.1, 33.07, 0.835 ],
            backgroundColor: ["#5ec8d8", "#5ec8d8", "#e8b34d"]
        }]
    }
});

animate(); 

