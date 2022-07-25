<template>
    <div class="Index">
        <div class="statistic">已复习:<span class="review">{{hasReview}}</span>/{{size}} 
        <!-- 今日: <span class="today">12</span>个 -->
        </div>
            <div class="row">
            <div :class="pos>0?'btn':'hidePrev'" @click="getPrev" class="prev">上一个</div>
            <div class="word">{{word.content}}</div>
            <div :class="word.userValue.length>0?'btn':'hidePrev'" @click="getNext" class="next btn">下一个</div>
        </div>
        <div class="translationList">
            <div class="translation">
                <div class=""></div>
                <input id="answerInput" autofocus type="text" v-model="word.userValue" placeholder="请输入释意" />
                <div v-if="showFakeInput" class="fakeInput" v-html="fakeInputValue"></div>
                <div class="size">{{word.userValue.length}}</div>
                <div :style="answerStyle" class="answer">
                    <div class="answer-value">{{word.answers}}</div>
                     <div v-if="showFakeInput" class="fake-answer-value"></div>
                    <div class="answer-devide"></div>
                </div>
               
            </div>
            
            
        </div>
        <div @touchstart="toggleAnswer" @touchcancel="toggleAnswer" @touchend="toggleAnswer" @mousedown="toggleAnswer" @mouseup="toggleAnswer" @mouseleave="toggleAnswer" class="answers">
            {{showAnswer?'按住':'查看答案'}}
        </div>
        

    </div>
    <div class="footer">
        <p>tips:</p>
        <p>电脑端方向键可切换单词 左右方向切换单词 下键查看答案 回车快速核对</p>
        <p>手机端再等等</p>

    </div>
</template>

<script setup>
// import { ref } from 'vue'
import { ref ,computed, reactive, onMounted} from 'vue'
import wordList from "@/storage/wordsList.json"

// import storageTool from "@/storage/storageTool.js"
// let st = storageTool()
// console.log(st)
// console.log(wordList)
const size = wordList.size
const showAnswer = ref(false)
const prevStack = []
const pos = ref(0)
const showFakeInput = ref(false)
const fakeInputValue = ref("")
const hasReview = ref(0)
hasReview.value = localStorage.length
const toggleAnswer = function(){
    showAnswer.value = !showAnswer.value
}
const word = reactive({
    content:"",
    answerList:["放弃"],
    userValue:"",
    index:""
})
const Lint = function(){
    let userList = word.userValue.split(" ")
    console.log(userList)
    for(let index in userList){
        let item = userList[index]
        let start =0
        let end = 0
        let pattenStart = 0
        let pattenEnd = 0
        let max = 0
        for(let i=0;i<item.length;i++){
            let answer = word.answers
            console.log(item,answer)
            let _end = i
            for(let j=0;j<answer.length;j++){
                if(item[_end]==answer[j]){
                    console.log(item[_end])
                    _end++
                    if(j!=answer.length-1)
                    continue
                }
                if(_end-i>max){
                    max = _end-i
                    start = i
                    end = _end
                    pattenStart = j-max 
                    pattenEnd = j
                }
            }
            
        }
        fakeInputValue.value += item.slice(0,start)
        fakeInputValue.value+= `<span class='active'>${item.slice(start,end)}</span>`
        fakeInputValue.value+=item.slice(end,)
        fakeInputValue.value+=" "
        console.log(start,end,item.slice(start,end))
        console.log(pattenStart,pattenEnd,word.answers.slice(pattenStart,pattenEnd))
        

    }
}
const getPrev = function(){
    if(pos.value>0){
        console.log(pos.value)
        pos.value--
        console.log(pos.value)
        getRandomWord(pos.value)
            // console.log(prevStack)
            // let rand = prevStack.pop()
            // getRandomWord(rand)
    }

}
const saveToStorage = function(word){
    localStorage.setItem(word.content,JSON.stringify(word))
}
const getNext = function(){
    if(word.userValue.length>0){
            saveToStorage(word)
    pos.value+=1
    getRandomWord()
    }

}
const getRandomWord = function(){
    let rand = 0
    if(pos.value>=prevStack.length){
       rand = parseInt(Math.random()*size ) 
    //    rand = 140
        prevStack.push(rand)
    }else{
        rand = prevStack[pos.value]
    }
    word.content = wordList["单词"][rand]
    let answers = wordList["释义"][rand]
    word.answers = answers
    word.userValue = ""
    word.index = rand
    fakeInputValue.value = ""
    console.log(pos.value,prevStack.length)
    hasReview.value = localStorage.length
}
const answerStyle= computed(()=>{
    if(showAnswer.value){
        return {
            width:"300px"
        }
    }else{
        return {
            width:"0px"
        }
    }
})
const openFakeInput = function(){
    if(showFakeInput.value==false){
        fakeInputValue.value =""
        showFakeInput.value = true
        Lint()
    }
    
}
const hideFakeInput = function(){
    showFakeInput.value = false
}
// const showPrev = computed(()=>{
//     if(prevStack.length>0){
//         return true
//     }else{
//         return false
//     }
// })
onMounted(()=>{
    getRandomWord()
    window.onkeydown = ()=>{
        let key = window.event.key
        if(key=="ArrowRight"){
            getNext()
        }else if(key == "ArrowLeft"){
            getPrev()
        }else if( key=="ArrowDown"){
            showAnswer.value = true
        }else if(key=="Enter"){
            openFakeInput()
        }
        
    }
    window.onkeyup = ()=>{
        let key = window.event.key
        if( key=="ArrowDown"){
            showAnswer.value = false
        }else if(key=="Enter"){
            hideFakeInput()
        }
    }
})
</script>
<style lang="scss" >
$defaultColor : #647372;
$activeColor : #42b983;
.statistic{
    color: grey;
    margin:15px 0;
    .review{
        color: crimson;
    }
    .today{
        color: $activeColor;
    }
}
.row {
    display: flex;
    justify-content: space-around;
}
.col{
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
    margin-top: 150px;
    height: 300px;
    overflow: auto;
    .translation {
        position: relative;
        width: 300px;
        margin: 0 auto;
        // background-color: #eee;
        margin-bottom: 20px;
        .fakeInput{
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
            top:0px;
        }
        input {
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
            transition: all 0.3s ease;
        }

        input:focus {
            outline: 2px solid $activeColor;
        }
        .size{
            position: absolute;
            right: 4px;
            top: 30px;
            font-size: 10px;
            color: grey;
        }
        .answer{
            margin:4px 0;
            text-align: left;
            width: 0;
            overflow: hidden;
            transition: width 0.3s ease;
            position: relative;
            &-value{
                width:300px;
                font-size: 14px;
            }
            .fake-answer-value{
                 width:300px;
                font-size: 14px;
                height: 20px;
                position: absolute;
                top:0;
                background-color: #fff;
            }
            &-devide{
                margin-top: 4px;
                width: 300px;
                height: 4px;
                background-color: #42b983;
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
.answers{
    color: $activeColor;
    font-size: 18px;
    cursor: pointer;
    margin-top:30px;
    // position: absolute;
    // bottom: 100px;
    // left:50%;
    // transform: translate(-50%,0);
}
.answers:active{
    color: crimson;
}
.footer {
    position: absolute;
    bottom: 30px;
    text-align: left;
    font-size: 12px;
    color: grey;
    margin-left: 1em;
    p {
        margin: 2px;
    }
}
.hidePrev{
    opacity: 0.5;
    cursor:not-allowed;
     padding: 5px 10px;
    border-radius: 5px;
    background-color: #eee;
    transition: background-color 0.3s ease;
    border: 2px solid #fff;
}
.active{
    background-color: #42b983;
}
</style>
