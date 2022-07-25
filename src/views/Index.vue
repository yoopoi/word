<template>
  <div class="Index">
    <div class="statistic">
      已复习:<span class="review">{{ hasReview }}</span
      >/{{ size }}
      <!-- 今日: <span class="today">12</span>个 -->
    </div>
    <div class="row">
      <div :class="pos > 0 ? 'btn' : 'hidePrev'" @click="getPrev" class="prev">
        上一个
      </div>
      <div class="word">{{ word.content }}</div>
      <div :class="hasLint ? 'btn' : 'hidePrev'" @click="getNext" class="next">
        下一个
      </div>
    </div>
    <div
      class="translationList"
      :style="{ margin: `${!showAnswer ? '150px' : '0'} 0 0 0` }"
    >
      <div class="translation">
        <input
          id="answerInput"
          autofocus
          type="text"
          v-model="word.userValue"
          @input="onInput"
          placeholder="请输入释义"
        />
        <div
          v-if="showFakeInput"
          class="fakeInput"
          v-html="fakeInputValue"
        ></div>
        <div class="size">{{ word.userValue.length }}</div>
        <div :style="answerStyle" class="answer">
          <template v-for="item in word.answers" v-bind:key="item">
            <div class="answer-sign" v-if="sign.indexOf(item) != -1">
              #{{ item }}
            </div>
            <div class="answer-value" v-else>{{ item }}</div>
          </template>
          <!-- <div v-if="showFakeInput" class="fake-answer-value"></div> -->
          <div class="answer-devide"></div>
        </div>
      </div>
    </div>
    <div
      @touchstart="showAnswerPanel"
      @touchcancel="closeAnswerPanel"
      @touchend="closeAnswerPanel"
      @mousedown="showAnswerPanel"
      @mouseup="closeAnswerPanel"
      class="answers"
    >
      {{ showAnswer ? "按住" : "查看答案" }}
    </div>
  </div>
  <div :style="{ opacity: `${!showAnswer ? '1' : '0'}` }" class="footer">
    <p>Tips:</p>
    <p>电脑端方向键可切换单词 左右方向切换单词 下键查看答案 回车快速核对</p>
    <p>手机端嘛...用默默背单词吧(●ˇ∀ˇ●)</p>
  </div>
</template>

<script setup>
// import { ref } from 'vue'
import { ref, computed, reactive, onMounted } from "vue";
import wordList from "@/storage/wordsList.json";

// import storageTool from "@/storage/storageTool.js"
// let st = storageTool()
// console.log(st)
// console.log(wordList)
const size = wordList.size;
const showAnswer = ref(false);
const prevStack = [];
const pos = ref(0);
const showFakeInput = ref(false);
const fakeInputValue = ref("");
const hasReview = ref(0);
hasReview.value = localStorage.length;
const sign = ["n", "adv", "adj", "v", "vt", "vi", "pron", "num", "conj"];
const hasLint = ref(false);
const showAnswerPanel = function () {
  showAnswer.value = true;
};
const closeAnswerPanel = function () {
  showAnswer.value = false;
};
const word = reactive({
  content: "",
  answerList: ["放弃"],
  userValue: "",
  index: "",
});
const Lint = function () {
  let flag = false;
  let userList = word.userValue.split(" ");

  console.log(userList);
  for (let index in userList) {
    let item = userList[index];
    if (word.answers.indexOf(item) != -1) {
      flag = true;
      fakeInputValue.value += `<span class='active'>${item}</span> `;
    }
  }
  hasLint.value = flag;
  return flag;
};
const getPrev = function () {
  if (pos.value > 0) {
    console.log(pos.value);
    pos.value--;
    console.log(pos.value);
    getRandomWord(pos.value);
    // console.log(prevStack)
    // let rand = prevStack.pop()
    // getRandomWord(rand)
  }
};
const onInput = function(){
    Lint()
}
const saveToStorage = function (word) {
  localStorage.setItem(word.content, JSON.stringify(word));
};
const getNext = function () {
  if (hasLint.value) {
    saveToStorage(word);
    pos.value += 1;
    getRandomWord();
  }
};
const getAnswerList = function (answers) {
  const re = /[\u4e00-\u9fa5_a-zA-Z0-9]+/g;
  var answerList = answers.match(re);
  console.log(answerList);
  return answerList;
};
const getRandomWord = function () {
  let rand = 0;
  if (pos.value >= prevStack.length) {
    rand = parseInt(Math.random() * size);
    //    rand = 140
    prevStack.push(rand);
  } else {
    rand = prevStack[pos.value];
  }

  word.content = wordList["单词"][rand];
  let answers = wordList["释义"][rand];
  word.answers = getAnswerList(answers);
  word.userValue = "";
  word.index = rand;
  hasLint.value = false;
  fakeInputValue.value = "";
  console.log(pos.value, prevStack.length);
  hasReview.value = localStorage.length;
};
const answerStyle = computed(() => {
  if (showAnswer.value) {
    return {
      maxHeight: "800px",
    };
  } else {
    return {
      maxHeight: "0px",
    };
  }
});
const openFakeInput = function () {
  if (showFakeInput.value == false) {
    fakeInputValue.value = "";
    showFakeInput.value = true;
    Lint();
  }
};
const hideFakeInput = function () {
  showFakeInput.value = false;
};
// const showPrev = computed(()=>{
//     if(prevStack.length>0){
//         return true
//     }else{
//         return false
//     }
// })
function mouseup() {
  closeAnswerPanel();
}
// function stop() {
//   document.body.style.height = "100vh";
//   document.body.style.overflow = "hidden";
//   document.addEventListener("touchmove", mo, false); //禁止页面滑动
// }
// var mo = function (e) {
//   e.preventDefault();
// };
onMounted(() => {
  getRandomWord();


  //直接默认不让滑动
//   stop();
    document.addEventListener("focusin",()=>{
        let interval = 1000
        let t1 = setInterval(()=>{
            document.documentElement.scrollTop =0
            window.scrollTop = 0
            interval-=30
            if(interval<0)clearInterval(t1)
        },30)
    },false)
  window.addEventListener("mouseup", mouseup, false);
  // 禁用双指放大
  document.documentElement.addEventListener(
    "touchstart",
    function (event) {
      if (event.touches.length > 1) {
        event.preventDefault();
      }
    },
    {
      passive: false,
    }
  );

  // 禁用双击放大
  var lastTouchEnd = 0;
  document.documentElement.addEventListener(
    "touchend",
    function (event) {
      var now = Date.now();
      if (now - lastTouchEnd <= 300) {
        event.preventDefault();
      }
      lastTouchEnd = now;
    },
    {
      passive: false,
    }
  );
  window.onkeydown = () => {
    let key = window.event.key;
    if (key == "ArrowRight") {
      getNext();
    } else if (key == "ArrowLeft") {
      getPrev();
    } else if (key == "ArrowDown") {
      showAnswer.value = true;
    } else if (key == "Enter") {
      openFakeInput();
    }
  };
  window.onkeyup = () => {
    let key = window.event.key;
    if (key == "ArrowDown") {
      showAnswer.value = false;
    } else if (key == "Enter") {
      hideFakeInput();
      if (hasLint.value) {
        setTimeout(() => {
          getNext();
        }, 500);
      }
    }
  };
});
</script>
<style lang="scss" >
$defaultColor: #647372;
$activeColor: #42b983;
$mainWidth: 300px;
.statistic {
  color: grey;
  display: inline-block;
  background-color: #eee;
  padding: 6px 12px;
  border-radius: 24px;
  margin: 15px 0;
  .review {
    color: crimson;
  }
  .today {
    color: $activeColor;
  }
}
.row {
  display: flex;
  justify-content: space-around;
}
.col {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: 100%;
}
.Index {
  width: 100%;
  user-select: none;
  height: 100vh;
  overflow: hidden;
  // background-color: #000;
}

.word {
  font-weight: bold;
  font-size: 24px;
}

.translationList {
  transition: margin 0.3s ease;
  //   height: 400px;
  overflow: auto;
  .translation {
    position: relative;
    width: 300px;
    margin: 0 auto;
    // background-color: #eee;
    margin-bottom: 20px;
    .fakeInput {
      margin-top: 4px;
      font-size: 18px;
      outline: 2px solid transparent;
      border: 2px solid #eee;
      width: 300px;
      height: 40px;
      line-height: 40px;
      text-align: center;
      background-color: #eee;
      border-radius: 5px;
      position: absolute;
      top: 0px;
    }
    input {
      margin-top: 4px;
      font-size: 18px;
      outline: 2px solid transparent;
      border: 2px solid #fff;
      width: 300px;
      height: 40px;
      line-height: 40px;
      text-align: center;
      background-color: #eee;
      border-radius: 5px;
      transition: all 0.3s ease;
    }

    input:focus {
      border: 2px solid $activeColor;
    }
    .size {
      position: absolute;
      right: 4px;
      top: 30px;
      font-size: 10px;
      color: grey;
    }
    .answer {
      margin: 4px 0;
      text-align: left;
      width: $mainWidth;
      overflow: hidden;
      transition: max-height 0.3s ease;
      position: relative;
      background-color: #fff;
      &-value {
        font-size: 14px;
        margin-left: 8px;
        padding: 3px 6px;
        background-color: #eee;
        border-radius: 3px;
        display: inline-block;
        word-wrap: normal;
        word-break: keep-all;
        white-space: nowrap;
        margin-bottom: 6px;
      }
      &-sign {
        margin-left: 8px;
        color: #42b983;
        font-size: 22px;
        margin-top: 6px;
      }
      .fake-answer-value {
        width: 300px;
        font-size: 14px;
        height: 20px;
        position: absolute;
        top: 0;
        background-color: #fff;
      }
      &-devide {
        margin-top: 4px;
        width: 4px;
        height: 300px;
        background-color: #42b983;
        position: absolute;
        left: 0;
        top: 0;
      }
    }
  }
}

.btn {
  padding: 5px 10px;
  border-radius: 5px;
  background-color: #eee;
  cursor: pointer;
  transition: background-color 0.3s ease;
  border: 2px solid #fff;
}

.btn:hover {
  background-color: $activeColor;
}

.btn:active {
  outline: 2px solid $activeColor;
}
.answers {
  color: $activeColor;
  font-size: 18px;
  cursor: pointer;
  //   margin-top: 30px;
  // position: absolute;
  // bottom: 100px;
  // left:50%;
  // transform: translate(-50%,0);
}
.answers:active {
  color: crimson;
}
.footer {
  user-select: none;
  position: absolute;
  bottom: 30px;
  text-align: left;
  font-size: 12px;
  color: grey;
  margin-left: 1em;
  transition: opacity 0.3s ease;
  p {
    margin: 2px;
  }
}
.hidePrev {
  opacity: 0.5;
  cursor: not-allowed;
  padding: 5px 10px;
  border-radius: 5px;
  background-color: #eee;
  transition: background-color 0.3s ease;
  border: 2px solid #fff;
}
.active {
  background-color: #42b983;
}
</style>
