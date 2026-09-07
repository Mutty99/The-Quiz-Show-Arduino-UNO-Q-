const socket = io();

const statusEl = document.getElementById("status");
const questionNumberEl = document.getElementById("question-number");
const questionTextEl = document.getElementById("question-text");
const scoreEl = document.getElementById("score");
const optionsRowEl = document.getElementById("options-row");
const scoreDisplayEl = document.getElementById("score-display");

const appContentEl = document.getElementById("app-content");

const bgmSlider = document.getElementById("bgm-volume");
const sfxSlider = document.getElementById("sfx-volume");

const feedbackBoxEl = document.getElementById("feedback-box");
const feedbackTextEl = document.getElementById("feedback-text");
const hiScoreValEl = document.getElementById("hi-score-val");
const newRecordBadgeEl = document.getElementById("new-record-badge");
const resultDescriptionEl = document.getElementById("result-description");

let currentSfxVolume = parseFloat(sfxSlider.value);

const bgmStart = new Audio("audio/bgm_start.ogg");
bgmStart.loop = true;
bgmStart.volume = parseFloat(bgmSlider.value);

const bgmQuiz = new Audio("audio/bgm.ogg");
bgmQuiz.loop = true;
bgmQuiz.volume = parseFloat(bgmSlider.value);

const bgmEnd = new Audio("audio/bgm_end.ogg");
bgmEnd.loop = true;
bgmEnd.volume = parseFloat(bgmSlider.value);

let currentBgm = bgmStart;
let currentResultAudio = null;

function switchTrack(newTrack) {
  if (currentBgm) {
    currentBgm.pause();
    currentBgm.currentTime = 0; 
  }
  currentBgm = newTrack;
  
  if (currentBgm) {
    currentBgm.play().catch(e => console.log("Autoplay bloccato dal browser:", e));
  }
}

bgmSlider.addEventListener("input", (e) => {
  const newVolume = parseFloat(e.target.value);
  bgmStart.volume = newVolume;
  bgmQuiz.volume = newVolume;
  bgmEnd.volume = newVolume; 
});

sfxSlider.addEventListener("input", (e) => {
  currentSfxVolume = parseFloat(e.target.value);
});

socket.on("connect",       () => { statusEl.className = "status connected";    statusEl.textContent = "● Connected";    });
socket.on("disconnect",    () => { statusEl.className = "status disconnected"; statusEl.textContent = "● Disconnected"; });
socket.on("connect_error", () => { statusEl.className = "status connecting";   statusEl.textContent = "Connecting…";  });

socket.on("play_bgm", (trackName) => {
  if (currentResultAudio) {
    currentResultAudio.pause();
    currentResultAudio.currentTime = 0;
    currentResultAudio = null;
  }
  
  if (trackName === "start") switchTrack(bgmStart);
  else if (trackName === "quiz") switchTrack(bgmQuiz);
});

socket.on("play_result_audio", (tier) => {
  if (currentBgm) {
    currentBgm.pause();
    currentBgm.currentTime = 0;
    currentBgm = null;
  }
  
  if (currentResultAudio) {
    currentResultAudio.pause();
  }
  currentResultAudio = new Audio(`audio/result${tier}.ogg`);
  currentResultAudio.volume = currentSfxVolume; 
  
  currentResultAudio.onended = () => {
    switchTrack(bgmEnd);
  };
  
  currentResultAudio.play().catch(e => console.log("Errore riproduzione audio finale:", e));
});

socket.on("play_sound", (result) => {
  let audio = null;
  if (result === "correct") audio = new Audio("audio/correct.ogg");
  else if (result === "wrong") audio = new Audio("audio/wrong.ogg");
  
  if (audio) {
    audio.volume = currentSfxVolume;
    audio.play().catch(e => console.log("Errore riproduzione audio:", e));
  }
});

socket.on("state_update", state => {
  if (state) {
    questionNumberEl.classList.remove("tier-0", "tier-1", "tier-2", "tier-3");
    
    if (state.start_screen) {
      questionNumberEl.classList.add("hidden");
      optionsRowEl.classList.add("hidden");
      scoreDisplayEl.classList.add("hidden");
      feedbackBoxEl.classList.add("hidden"); 
      resultDescriptionEl.classList.add("hidden"); 
      
    } else if (state.wait_result) {
      questionNumberEl.textContent = "Quiz Complete!";
      questionNumberEl.classList.remove("hidden");
      optionsRowEl.classList.add("hidden");
      scoreDisplayEl.classList.remove("hidden");
      resultDescriptionEl.classList.add("hidden");
      if (state.last_result !== null) feedbackBoxEl.classList.remove("hidden");

    } else if (state.game_over) {
      questionNumberEl.textContent = state.result_title;
      questionNumberEl.classList.add(`tier-${state.result_tier}`);
      questionNumberEl.classList.remove("hidden");
      optionsRowEl.classList.add("hidden");
      scoreDisplayEl.classList.remove("hidden");
      resultDescriptionEl.textContent = state.result_desc;
      resultDescriptionEl.classList.remove("hidden");
      feedbackBoxEl.classList.add("hidden");
      
    } else {
      questionNumberEl.textContent = `Question ${state.current_q + 1}`;
      questionNumberEl.classList.remove("hidden");
      optionsRowEl.classList.remove("hidden");
      scoreDisplayEl.classList.remove("hidden");
      resultDescriptionEl.classList.add("hidden"); 
      if (state.last_result === null) {
        feedbackBoxEl.classList.add("hidden");
      } else {
        feedbackBoxEl.classList.remove("hidden");
      }
    }
    
    questionTextEl.textContent = state.question_text;
    scoreEl.textContent = state.score;
    hiScoreValEl.textContent = state.highest_score;
    
    for(let i = 0; i < 3; i++) {
        document.getElementById(`option-${i}`).textContent = state.options[i];
    }

    if (state.new_record) {
      newRecordBadgeEl.classList.remove("hidden");
    } else {
      newRecordBadgeEl.classList.add("hidden");
    }

    if (state.last_result !== null) {
      if (state.last_result === true) {
        feedbackTextEl.textContent = "Correct! :D";
        feedbackTextEl.className = "text-correct"; 
      } else {
        feedbackTextEl.textContent = `Wrong... it was ${state.last_correct_letter}! :(`;
        feedbackTextEl.className = "text-wrong"; 
      }
    }
  }
});