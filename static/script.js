// ---------------------------------------------------------
// Tab switching
// ---------------------------------------------------------
const railTabs = document.querySelectorAll(".rail-tab");
railTabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    railTabs.forEach((t) => t.classList.remove("active"));
    document.querySelectorAll(".panel").forEach((p) => p.classList.remove("active"));

    tab.classList.add("active");
    const target = tab.dataset.tab;
    document.getElementById(`panel-${target}`).classList.add("active");
  });
});

// ---------------------------------------------------------
// Helpers
// ---------------------------------------------------------
function setLoading(el, message) {
  el.className = "output loading";
  el.textContent = message;
}

function setError(el, message) {
  el.className = "output error";
  el.textContent = `⚠️ ${message}`;
}

function setText(el, label, text) {
  el.className = "output";
  el.innerHTML = `<span class="label">${label}</span>${escapeHtml(text)}`;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// ---------------------------------------------------------
// Q&A
// ---------------------------------------------------------
document.getElementById("qaForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = document.getElementById("question").value;
  const resultEl = document.getElementById("qaResult");
  setLoading(resultEl, "Thinking...");

  try {
    const res = await fetch(`/qa?question=${encodeURIComponent(question)}`);
    const data = await res.json();
    if (data.answer) {
      setText(resultEl, "Answer", data.answer);
    } else {
      setError(resultEl, data.error || "Something went wrong.");
    }
  } catch (err) {
    setError(resultEl, "Could not reach the server.");
  }
});

// ---------------------------------------------------------
// Explanation
// ---------------------------------------------------------
document.getElementById("explainForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const topic = document.getElementById("topic").value;
  const resultEl = document.getElementById("explainResult");
  setLoading(resultEl, "Preparing a simple explanation...");

  try {
    const res = await fetch("/explain/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic }),
    });
    const data = await res.json();
    if (data.explanation) {
      setText(resultEl, "Explanation", data.explanation);
    } else {
      setError(resultEl, data.error || "Something went wrong.");
    }
  } catch (err) {
    setError(resultEl, "Could not reach the server.");
  }
});

// ---------------------------------------------------------
// Summary
// ---------------------------------------------------------
document.getElementById("summaryForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = document.getElementById("summaryText").value;
  const resultEl = document.getElementById("summaryResult");
  setLoading(resultEl, "Summarizing...");

  try {
    const res = await fetch("/summarize/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    if (data.summary) {
      setText(resultEl, "Summary", data.summary);
    } else {
      setError(resultEl, data.error || "Something went wrong.");
    }
  } catch (err) {
    setError(resultEl, "Could not reach the server.");
  }
});

// ---------------------------------------------------------
// Learning Path
// ---------------------------------------------------------
document.getElementById("learnForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const topic = document.getElementById("learnTopic").value;
  const resultEl = document.getElementById("learnResult");
  setLoading(resultEl, "Building your learning path...");

  try {
    const res = await fetch(`/learn/recommendations?topic=${encodeURIComponent(topic)}`);
    const data = await res.json();
    if (data.recommendation) {
      setText(resultEl, `Learning Path — ${data.topic}`, data.recommendation);
    } else {
      setError(resultEl, data.error || "Something went wrong.");
    }
  } catch (err) {
    setError(resultEl, "Could not reach the server.");
  }
});

// ---------------------------------------------------------
// Quiz (interactive: click an option, get instant feedback)
// ---------------------------------------------------------
document.getElementById("quizForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = document.getElementById("quizText").value;
  const resultEl = document.getElementById("quizResult");
  setLoading(resultEl, "Generating quiz questions...");

  try {
    const res = await fetch("/quiz", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    const quiz = data.quiz;

    if (!Array.isArray(quiz) || quiz.length === 0 || quiz[0].error) {
      setError(resultEl, (quiz && quiz[0] && quiz[0].error) || "Could not generate a quiz.");
      return;
    }

    renderQuiz(resultEl, quiz);
  } catch (err) {
    setError(resultEl, "Could not reach the server.");
  }
});

function renderQuiz(container, quiz) {
  container.className = "output quiz-output";
  container.innerHTML = "";

  quiz.forEach((q, qIndex) => {
    const block = document.createElement("div");
    block.className = "quiz-question";

    const qText = document.createElement("p");
    qText.className = "q-text";
    qText.textContent = `Q${qIndex + 1}: ${q.question}`;
    block.appendChild(qText);

    const optionsWrap = document.createElement("div");
    let selected = null;

    q.options.forEach((opt) => {
      const optLabel = document.createElement("label");
      optLabel.className = "quiz-option";
      optLabel.innerHTML = `
        <input type="radio" name="q${qIndex}" value="${escapeHtml(opt)}" />
        <span>${escapeHtml(opt)}</span>
      `;
      optLabel.querySelector("input").addEventListener("change", (e) => {
        selected = e.target.value;
      });
      optionsWrap.appendChild(optLabel);
    });
    block.appendChild(optionsWrap);

    const checkBtn = document.createElement("button");
    checkBtn.className = "check-btn";
    checkBtn.textContent = "Check Answer";
    checkBtn.type = "button";

    const feedback = document.createElement("div");
    feedback.className = "quiz-feedback";

    checkBtn.addEventListener("click", () => {
      if (!selected) {
        feedback.textContent = "Please select an option first.";
        feedback.className = "quiz-feedback incorrect";
        return;
      }
      if (selected === q.answer) {
        feedback.textContent = "✅ Correct!";
        feedback.className = "quiz-feedback correct";
      } else {
        feedback.textContent = `❌ Incorrect. Correct answer: ${q.answer}`;
        feedback.className = "quiz-feedback incorrect";
      }
    });

    block.appendChild(checkBtn);
    block.appendChild(feedback);
    container.appendChild(block);
  });
}
