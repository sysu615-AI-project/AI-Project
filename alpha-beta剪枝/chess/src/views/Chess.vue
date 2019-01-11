<template>
  <div class="chess" ref="chess">
      <h1>中&nbsp;&nbsp;国&nbsp;&nbsp;象&nbsp;&nbsp;棋</h1>
      <div class="chessBoard" @click="turnToPlayer && imgClick($event)" v-if="restart">
        <img id="BR1" ref="BR1" src="../assets/chesses/BR.png"/>
        <img id="BN1" ref="BN1" src="../assets/chesses/BN.png"/>
        <img id="BB1" ref="BB1" src="../assets/chesses/BB.png"/>
        <img id="BA1" ref="BA1" src="../assets/chesses/BA.png"/>
        <img id="BK" ref="BK" src="../assets/chesses/BK.png"/>
        <img id="BA2" ref="BA2" src="../assets/chesses/BA.png"/>
        <img id="BB2" ref="BB2" src="../assets/chesses/BB.png"/>
        <img id="BN2" ref="BN2" src="../assets/chesses/BN.png"/>
        <img id="BR2" ref="BR2" src="../assets/chesses/BR.png"/>
        <img id="BC1" ref="BC1" src="../assets/chesses/BC.png"/>
        <img id="BC2" ref="BC2" src="../assets/chesses/BC.png"/>
        <img id="BP1" ref="BP1" src="../assets/chesses/BP.png"/>
        <img id="BP2" ref="BP2" src="../assets/chesses/BP.png"/>
        <img id="BP3" ref="BP3" src="../assets/chesses/BP.png"/>
        <img id="BP4" ref="BP4" src="../assets/chesses/BP.png"/>
        <img id="BP5" ref="BP5" src="../assets/chesses/BP.png"/>

        <img id="RP1" ref="RP1" src="../assets/chesses/RP.png"/>
        <img id="RP2" ref="RP2" src="../assets/chesses/RP.png"/>
        <img id="RP3" ref="RP3" src="../assets/chesses/RP.png"/>
        <img id="RP4" ref="RP4" src="../assets/chesses/RP.png"/>
        <img id="RP5" ref="RP5" src="../assets/chesses/RP.png"/>
        <img id="RC1" ref="RC1" src="../assets/chesses/RC.png"/>
        <img id="RC2" ref="RC2" src="../assets/chesses/RC.png"/>
        <img id="RR1" ref="RR1" src="../assets/chesses/RR.png"/>
        <img id="RN1" ref="RN1" src="../assets/chesses/RN.png"/>
        <img id="RB1" ref="RB1" src="../assets/chesses/RB.png"/>
        <img id="RA1" ref="RA1" src="../assets/chesses/RA.png"/>
        <img id="RK" ref="RK" src="../assets/chesses/RK.png"/>
        <img id="RA2" ref="RA2" src="../assets/chesses/RA.png"/>
        <img id="RB2" ref="RB2" src="../assets/chesses/RB.png"/>
        <img id="RN2" ref="RN2" src="../assets/chesses/RN.png"/>
        <img id="RR2" ref="RR2" src="../assets/chesses/RR.png"/>
      </div>
      <div id="Loading" v-if="!restart">
        <div class="loader-inner ball-beat">
          <div></div>
          <div></div>
          <div></div>
        </div>
      </div>
      <div class="MsgDiv" v-if="end">
        <p>
          {{ endInfo }}
        </p>
        <button @click="reset">再来一局</button>
      </div>
  </div>
</template>

<script>
export default{
  data () {
    return {
      INT_MAX: 99999999999,
      INT_MIN: -1*99999999999,
      turnToPlayer: true,
      selected: null,
      chessWidth: 40,
      chessHeight: 40,
      redRiverDimen: 5,
      redJiuGongLeft: 3,
      redJiuGongRight: 5,
      redJiuGongTop: 7,
      blackRiverDimen: 4,
      blackJiuGongLeft: 3,
      blackJiuGongRight: 5,
      blackJiuGongBottom: 2,
      red: "R",
      black: "B",
      depth: 4,
      end: false,
      endInfo: "",
      restart: true,
      opponent: {
        "R": "B",
        "B": "R"
      },
      bestStep: {},
      chessBoard: [
        ["BR1","BN1","BB1","BA1","BK","BA2","BB2","BN2","BR2"],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0,"BC1", 0, 0, 0, 0, 0,"BC2", 0],
        ["BP1", 0,"BP2", 0,"BP3", 0,"BP4", 0,"BP5"],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["RP1", 0,"RP2", 0,"RP3", 0,"RP4", 0,"RP5"],
        [0,"RC1", 0, 0, 0, 0, 0,"RC2", 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["RR1","RN1","RB1","RA1","RK","RA2","RB2","RN2","RR2"]
      ],
      chessValue: {
        "K": 100000,
        "A": 110,
        "B": 110,
        "N": 300,
        "R": 500,
        "C": 300,
        "P": 100
      },
      // 控制区域价值
      chessPosValue: {
        'P': [
          [0, 3, 6, 9, 12, 9, 6, 3, 0],
          [18, 36, 56, 80, 120, 80, 56, 36, 18],
          [14, 26, 42, 60, 80, 60, 42, 26, 14],
          [10, 20, 30, 34, 40, 34, 30, 20, 10],
          [6, 12, 18, 18, 20, 18, 18, 12, 6],
          [2, 0, 8, 0, 8, 0, 8, 0, 2],
          [0, 0, -2, 0, 4, 0, -2, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        'R': [
          [14, 14, 12, 18, 16, 18, 12, 14, 14],
          [16, 20, 18, 24, 26, 24, 18, 20, 16],
          [12, 12, 12, 18, 18, 18, 12, 12, 12],
          [12, 18, 16, 22, 22, 22, 16, 18, 12],
          [12, 14, 12, 18, 18, 18, 12, 14, 12],
          [12, 16, 14, 20, 20, 20, 14, 16, 12],
          [6, 10, 8, 14, 14, 14, 8, 10, 6],
          [4, 8, 6, 14, 12, 14, 6, 8, 4],
          [8, 4, 8, 16, 8, 16, 8, 4, 8],
          [-1, 10, 6, 14, 12, 14, 6, 10, -2],
        ],
        'N': [
          [4, 8, 16, 12, 4, 12, 16, 8, 4],
          [4, 10, 28, 16, 8, 16, 28, 10, 4],
          [12, 14, 16, 20, 18, 20, 16, 14, 12],
          [8, 24, 18, 24, 20, 24, 18, 24, 8],
          [6, 16, 14, 18, 16, 18, 14, 16, 6],
          [4, 12, 16, 14, 12, 14, 16, 12, 4],
          [2, 6, 8, 6, 10, 6, 8, 6, 2],
          [4, 2, 8, 8, 4, 8, 8, 2, 4],
          [0, 2, 4, 4, -2, 4, 4, 2, 0],
          [0, -4, 0, 0, 0, 0, 0, -4, 0],
        ],
        'C': [
          [6, 4, 0, -10, -12, -10, 0, 4, 6],
          [2, 2, 0, -4, -14, -4, 0, 2, 2],
          [2, 2, 0, -10, -8, -10, 0, 2, 2],
          [0, 0, -2, 4, 10, 4, -2, 0, 0],
          [0, 0, 0, 2, 8, 2, 0, 0, 0],
          [-2, 0, 4, 2, 6, 2, 4, 0, -2],
          [0, 0, 0, 2, 4, 2, 0, 0, 0],
          [4, 0, 8, 6, 10, 6, 8, 0, 4],
          [0, 2, 4, 6, 6, 6, 4, 2, 0],
          [0, 0, 2, 6, 6, 6, 2, 0, 0],
        ],
      }
    }
  },
  mounted() {
  },
  methods: {
    min_max(a, b) {
      if(a<b) {
        return {"min": a, "max": b}
      }
      return {"min": b, "max": a}
    },
    formatPos: function(pos) {
      pos.x = Math.round((Math.round(pos.x / this.chessWidth - 1) * this.chessWidth + 8) / this.chessWidth)
      pos.y = Math.round((Math.round(pos.y / this.chessHeight - 1) * this.chessHeight + 8) / this.chessHeight)
      return pos
    },
    realPos: function(pos) {
      pos.x = pos.x * this.chessWidth + 8;
      pos.y = pos.y * this.chessHeight + 8;
      return pos
    },
    swap: function(chessBoard, from, to) {
      chessBoard[to.y][to.x] = chessBoard[from.y][from.x]
      chessBoard[from.y][from.x] = 0
    },
    displayChessBoard: function(chessBoard) {
      console.log("#########chessTable##########")
      for(let i=0; i<10; i++){
        console.log(JSON.stringify(chessBoard[i]))
      }
    },
    getTarget: function(chessBoard, to) {
      let target = null
      if((to.y >= 0 && to.y < 10) && (to.x >= 0 && to.x < 9) && chessBoard[to.y][to.x]!=0) {
        target = this.$refs[chessBoard[to.y][to.x]]
      }
      return target
    },
    ending: function(id) {
      this.turnToPlayer=false
      this.end=true
      switch(id){
        case "BK":
          this.endInfo = "You Win!"
          break
        case "RK":
          this.endInfo = "You Lose!"
          break
      }
    },
    reset: function() {
      this.restart=false
      setTimeout(()=> {
        Object.assign(this.$data, this.$options.data())
      }, 500)
    },
    // 帅与将 不能正对
    check: function() {
      let posBK = this.formatPos({"x": this.$refs["BK"].offsetLeft + this.chessWidth/2, "y": this.$refs["BK"].offsetTop + this.chessHeight/2})
      let posRK = this.formatPos({"x": this.$refs["RK"].offsetLeft + this.chessWidth/2, "y": this.$refs["RK"].offsetTop + this.chessHeight/2})
      if(posBK.x == posRK.x) {
        let count = 0
        for(let i=posBK.y+1; i<posRK.y-1; i++) {
          if(this.chessBoard[i][posBK.x] != 0) {
            count++
          }
        }
        if(count > 0) {
          return false
        }
        return true
      }
      return false
    },
    validMove: function(chessBoard, id, from, to) {
      switch(id.slice(0, 2)) {
        // 兵
        case "RP":
          if(to.x === from.x && from.y - to.y === 1) {
            return true
          } else if (to.y === from.y && Math.abs(to.x - from.x) === 1) {
            if(from.y < this.redRiverDimen) {
              return true
            }
          }
          return false
        case "BP":
          if(to.x === from.x && from.y - to.y === -1) {
            return true
          } else if (to.y === from.y && Math.abs(to.x - from.x) === 1) {
            if(from.y > this.blackRiverDimen) {
              return true
            }
          }
          return false
        // 砲
        case "RC":
        case "BC":
          if(to.x == from.x || to.y == from.y) {
            let count = 0
            if(to.x == from.x) {
              let res = this.min_max(from.y, to.y)
              for(let i=res.min + 1; i<res.max; i++) {
                if(chessBoard[i][to.x] != 0) {
                  count++
                }
              }
            } else {
              let res = this.min_max(from.x, to.x)
              for(let i=res.min + 1; i<res.max; i++) {
                if(chessBoard[from.y][i] != 0) {
                  count++
                }
              }
            }
            if(this.getTarget(chessBoard, to) != null) {
              if(this.getTarget(chessBoard, to).id[0] === this.opponent[id[0]]) {
                return count == 1
              } else {
                return false
              }
            } else {
              return count == 0
            }
          }
          return false
        // 車
        case "RR":
        case "BR":
          if(to.x == from.x || to.y == from.y) {
            let count = 0
            if(to.x == from.x) {
              let res = this.min_max(from.y, to.y)
              for(let i=res.min + 1; i<res.max; i++) {
                if(chessBoard[i][to.x] != 0) {
                  count++
                }
              }
            } else {
              let res = this.min_max(from.x, to.x)
              for(let i=res.min + 1; i<res.max; i++) {
                if(chessBoard[from.y][i] != 0) {
                  count++
                }
              }
            }
            if(this.getTarget(chessBoard, to) != null) {
              if(this.getTarget(chessBoard, to).id[0] === this.opponent[id[0]]) {
                return count == 0
              } else {
                return false
              }
            } else {
              return count == 0
            }
          }
          return false
        // 馬
        case "RN":
        case "BN":
          if(this.getTarget(chessBoard, to)!=null) {
            if(this.getTarget(chessBoard, to).id[0] === id[0]) {
              return false
            }
          }
          // 顺时针：上、右、下、左
          // 上
          if(to.y == from.y-2 && (to.x == from.x-1 || to.x == from.x+1)) {
            return this.getTarget(chessBoard, {"x": from.x, "y": from.y-1}) == null
          }
          // 右
          if(to.x == from.x+2 && (to.y == from.y-1 || to.y == from.y+1)) {
            return this.getTarget(chessBoard, {"x": from.x+1, "y": from.y}) == null
          }
          // 下
          if(to.y == from.y+2 && (to.x == from.x+1 || to.x == from.x-1)) {
            return this.getTarget(chessBoard, {"x": from.x, "y": from.y+1}) == null
          }
          // 左
          if(to.x == from.x-2 && (to.y == from.y+1 || to.y == from.y-1)) {
            return this.getTarget(chessBoard, {"x": from.x-1, "y": from.y}) == null
          }
          return false
        // 相
        case "RB":
          // 不能过河
          if(to.y < this.redRiverDimen){
            return false
          }
        case "BB":
          if(id[0] == this.black && to.y > this.blackRiverDimen) {
            return false
          }
          if(this.getTarget(chessBoard, to)!=null) {
            if(this.getTarget(chessBoard, to).id[0] == id[0]) {
              return false
            }
          }
          // 顺时针: 右上、右下、左下、左上
          // 右上
          if(to.y == from.y-2 && to.x == from.x+2) {
            return this.getTarget(chessBoard, {"x": from.x+1, "y": from.y-1}) == null
          }
          // 右下
          if(to.y == from.y+2 && to.x == from.x+2) {
            return this.getTarget(chessBoard, {"x": from.x+1, "y": from.y+1}) == null
          }
          // 左下
          if(to.y == from.y+2 && to.x == from.x-2) {
            return this.getTarget(chessBoard, {"x": from.x-1, "y": from.y+1}) == null
          }
          // 左上
          if(to.y == from.y-2 && to.x == from.x-2) {
            return this.getTarget(chessBoard, {"x": from.x-1, "y": from.y-1}) == null
          }
          return false
        // 仕
        case "RA":
          // 不能出九宫
          if(to.y < this.redJiuGongTop || to.x<this.redJiuGongLeft || to.x > this.redJiuGongRight){
            return false
          }
        case "BA":
          if(id[0] == this.black && (to.y > this.blackJiuGongBottom || to.x<this.blackJiuGongLeft || to.x > this.blackJiuGongRight)) {
            return false
          }
          if(this.getTarget(chessBoard, to)!=null) {
            if(this.getTarget(chessBoard, to).id[0] == id[0]) {
              return false
            }
          }
          // 顺时针：右上、右下、左下、左上
          // 右上
          if(to.y == from.y-1 && to.x == from.x+1) {
            return true
          }
          // 右下
          if(to.y == from.y+1 && to.x == from.x+1) {
            return true
          }
          // 左下
          if(to.y == from.y+1 && to.x == from.x-1) {
            return true
          }
          // 左上
          if(to.y == from.y-1 && to.x == from.x-1) {
            return true
          }
          return false
        // 帥
        case "RK":
          // 不能出九宫
          if(this.check()){
            return true
          }
          if(to.y < this.redJiuGongTop || to.x<this.redJiuGongLeft || to.x > this.redJiuGongRight){
            return false
          }

        case "BK":
          if(id[0] == this.black && this.check()){
            return true
          }
          if(id[0] == this.black && (to.y > this.blackJiuGongBottom || to.x<this.blackJiuGongLeft || to.x > this.blackJiuGongRight)) {
            return false
          }
          if(this.getTarget(chessBoard, to)!=null) {
            if(this.getTarget(chessBoard, to).id[0] == id[0]) {
              return false
            }
          }
          if(to.y == from.y && (to.x == from.x+1 || to.x == from.x-1)) {
            return true
          }
          if(to.x == from.x && (to.y == from.y+1 || to.y == from.y-1)) {
            return true
          }
          return false
      }
      return false
    },
    move: function(selected, from, to) {
      let target = this.getTarget(this.chessBoard, to)
      this.swap(this.chessBoard, from, to)
      to = this.realPos(to)
      // document.getElementById(selected.id).setAttribute("style", "top:"+to.y+"px;left:"+to.x+"px")
      selected.style.top = to.y+"px"
      selected.style.left = to.x+"px"
      // selected.style.transition = "all 0.5s"
      if(target != null) {
        // setTimeout(() => {
          target.style.display = "none"
        // }, 200)
      }
      if(target!=null && (target.id === "BK" || target.id === "RK")) {
        this.ending(target.id)
      }
    },
    getCopy: function(array) {
      let re=[];
      for(let i=0;i<array.length;i++){
        let [...arr]=array[i];
        re.push(arr);
      }
      return re
    },
    updateDepth: function() {
      let count = 0
      for(let i=0; i<10; i++) {
        for(let j=0; j<9; j++) {
          if(this.chessBoard[i][j] != 0) {
            count++
          }
        }
      }
      if(count < 6) {
        this.depth = 6
      } else if(count < 15) {
        this.depth = 5
      } else if(count < 28) {
        this.depth = 4
      }
      return count
    },
    imgClick: function(event) {
      let from = {}, to = {} 
      if(this.selected == null && event.target.id.indexOf("R") === 0) {
        // console.log("select")
        event.target.className = "OOS"
        this.selected = event.target
        return
      } else if (this.selected != null && event.target.id.indexOf("R") === 0) {
        // console.log("change select")
        if(this.selected.id != event.target.id) {
          event.target.className = "OOS"
          this.selected.className = ""
          this.selected = event.target
        } else {
          this.selected.className = ""
          this.selected=null
        }
      } else if(this.selected != null && event.target.id.indexOf("B") === 0) {
        // console.log("try to eat")
        from = this.formatPos({"x": this.selected.offsetLeft + this.chessWidth/2, "y": this.selected.offsetTop + this.chessWidth/2})
        to = this.formatPos({"x": event.target.offsetLeft + this.chessWidth/2, "y": event.target.offsetTop + this.chessHeight/2})
        if(this.validMove(this.chessBoard, this.selected.id, from, to)) {
          this.move(this.selected, from, to)
          this.selected.className = ""
          this.selected = null
          this.updateDepth()
          this.robot()
        }
      } else if(this.selected != null) {
        // console.log("move")
        from = this.formatPos({"x": this.selected.offsetLeft + this.chessWidth/2, "y": this.selected.offsetTop + this.chessWidth/2})
        to = this.formatPos({"x": event.layerX, "y": event.layerY})
        if(this.validMove(this.chessBoard, this.selected.id, from, to)) {
          this.move(this.selected, from, to)
          this.selected.className = ""
          this.selected = null
          this.updateDepth()
          this.robot()
        }
      }
    },
    robot: function() {
      this.turnToPlayer = false
      this.robotNextStep(this.getCopy(this.chessBoard), this.black, this.INT_MIN, this.INT_MAX, 1);
      // this.displayChessBoard(this.chessBoard)
      this.move(this.$refs[this.bestStep.id], this.bestStep.from, this.bestStep.to)
      this.turnToPlayer = true
      // this.displayChessBoard(this.chessBoard)
    },
    evaluation: function(chessBoard) {
      let blackValue =0, redValue=0, tos=[], target
      // console.log("evaluation in: ", chessBoard)
      for(let i=0;i<10;i++) {
        for(let j=0;j<9;j++) {
          if(chessBoard[i][j]!=0) {
            if(chessBoard[i][j][0] == this.black) {
              blackValue += this.chessValue[chessBoard[i][j][1]]
              if(this.chessPosValue[chessBoard[i][j][1]] != undefined) {
                blackValue += this.chessPosValue[chessBoard[i][j][1]][9-i][j] * 8
              }
              // tos = this.generateNextStep(chessBoard, {"x": j, "y": i})
              // for(let k=0, len=tos.length; k<len; k++) {
              //   target = this.getTarget(chessBoard, tos[k])
              //   if(target != null && target.id[0] == this.red && this.validMove(chessBoard, chessBoard[i][j], {"x": j, "y": i}, tos[k])) {
              //     redValue -= this.chessValue[target.id[1]]
              //   }
              // }
            } else {
              redValue += this.chessValue[chessBoard[i][j][1]]
              if(this.chessPosValue[chessBoard[i][j][1]] != undefined) {
                redValue += this.chessPosValue[chessBoard[i][j][1]][i][j] * 8
              }
              // tos = this.generateNextStep(chessBoard, {"x": j, "y": i})
              // for(let k=0, len=tos.length; k<len; k++) {
              //   target = this.getTarget(chessBoard, tos[k])
              //   if(target!=null && target.id[0] == this.black && this.validMove(chessBoard, chessBoard[i][j], {"x": j, "y": i}, tos[k])) {
              //     blackValue -= this.chessValue[target.id[1]]
              //   }
              // }
            }
          }
        }
      }
      // console.log("evaluation out: ", blackValue - redValue)
      return blackValue - redValue
    },
    generateNextStep: function(chessBoard, from) {
      let tos = [], to
      for(let i=0; i<10; i++) {
        for(let j=0; j<9; j++) {
          to = {"x": j, "y": i}
          if(this.validMove(chessBoard, chessBoard[from.y][from.x], from, to)) {
            tos.push(to)
          }
        }
      }
      return tos
    },
    robotNextStep: function(chessBoard, turn, alpha, beta, step) {
      // console.log("step"+step)
      if(step >= this.depth) {
        return this.evaluation(chessBoard)
      }
      // this.displayChessBoard(chessBoard)
      let value, nextStep = {}, from
      for(let i=0; i<10; i++) {
        for(let j=0; j<9; j++) {
          if(chessBoard[i][j] == 0) {
            continue
          }
          if(chessBoard[i][j].indexOf(turn) === 0) {
            from = {"x": j, "y": i}
            let [...tos] = this.generateNextStep(chessBoard, from), temp
            // console.log(chessBoard[i][j], "from: ", from, "tos: ", tos)
            for(let k=0, len = tos.length; k<len; k++) {
              // this.displayChessBoard(chessBoard)
              temp = chessBoard[tos[k].y][tos[k].x]
              this.swap(chessBoard, from, tos[k])
              // this.displayChessBoard(chessBoard)
              if(turn == this.black) {
                value = this.robotNextStep(this.getCopy(chessBoard), this.red, alpha, beta, step+1)
                if(value > alpha) {
                  alpha = value
                  nextStep.id = chessBoard[tos[k].y][tos[k].x]
                  nextStep.from = from
                  nextStep.to = tos[k]
                }
                if(alpha > beta) {
                  return beta
                }
              } else {
                value = this.robotNextStep(this.getCopy(chessBoard), this.black, alpha, beta, step+1)
                if(value < beta) {
                  beta = value
                  nextStep.id = chessBoard[tos[k].y][tos[k].x]
                  nextStep.from = from
                  nextStep.to = tos[k]
                }
                if(beta < alpha) {
                  return alpha
                }
              }
              this.swap(chessBoard, tos[k], from)
              chessBoard[tos[k].y][tos[k].x] = temp
            }
          }
        }
      }
      this.bestStep = nextStep
      return value
    }
  }
}
</script>
<style scoped>
  .chess{
    margin: auto;
    width: 377px;
    height: 600px;
  }
  .chessBoard {
    position: relative;
    margin: auto;
    width: 377px;
    height: 417px;
    background: url("../assets/chessBoard.png") no-repeat;
  }
  .slider{
    transition: all 0.5s;
    -webkit-transition: all 0.5s;
    /* transition-timing-function: cubic-bezier(0, 1, 0.5, 1); */
  }
  img {
    position: absolute;
    /* transition: all 0.2s; */
  }
  .OOS {
    background: url("../assets/chesses/OOS.png")
  }
  button {
    width: 100px;
    height: 40px;
    color: #279fcf;
  }
  #Loading {
    position: absolute;
    top:40%;
    left:50%;
    -webkit-transform: translateY(-50%)  translateX(-50%);
    transform: translateY(-50%)  translateX(-50%);
    z-index:100;
  }
  @-webkit-keyframes ball-beat {
    50% {
      opacity: 0.2;
      -webkit-transform: scale(0.75);
      transform: scale(0.75); 
    }
    100% {
      opacity: 1;
      -webkit-transform: scale(1);
      transform: scale(1); 
    } 
  }
  @keyframes ball-beat {
    50% {
      opacity: 0.2;
      -webkit-transform: scale(0.75);
      transform: scale(0.75); 
    }
    100% {
      opacity: 1;
      -webkit-transform: scale(1);
      transform: scale(1); 
    } 
  }

  .ball-beat > div {
    background-color: #279fcf;
    width: 15px;
    height: 15px;
    border-radius: 100% !important;
    margin: 2px;
    -webkit-animation-fill-mode: both;
    animation-fill-mode: both;
    display: inline-block;
    -webkit-animation: ball-beat 0.7s 0s infinite linear;
    animation: ball-beat 0.7s 0s infinite linear; 
  }
  .ball-beat > div:nth-child(2n-1) {
    -webkit-animation-delay: 0.35s !important;
    animation-delay: 0.35s !important;
  }
  .MsgDiv {
    position: fixed;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    z-index: 3;
  }

  .MsgDiv p {
    margin-top: 600px;
    opacity: 1;
    font-size: 20px;
    padding: 0px;
    color: red;
    text-align: center;
  }
  #BP1 {
    top: 128px;
    left: 8px;
  }
  #BP2 {
    top: 128px;
    left: 88px;
  }
  #BP3 {
    top: 128px;
    left: 168px;
  }
  #BP4 {
    top: 128px;
    right: 88px;
  }
  #BP5 {
    top: 128px;
    right: 8px;
  }
  #BC1 {
    top: 88px;
    left: 48px;
  }
  #BC2 {
    top: 88px;
    right: 48px;
  }
  #BR1 {
    top: 8px;
    left: 8px;
  }
  #BR2 {
    top: 8px;
    right: 8px;
  }
  #BN1 {
    top: 8px;
    left: 48px;
  }
  #BN2 {
    top: 8px;
    right: 48px;
  }
  #BB1 {
    top: 8px;
    left: 88px;
  }
  #BB2 {
    top: 8px;
    right: 88px;
  }
  #BA1 {
    top: 8px;
    left: 128px;
  }
  #BA2 {
    top: 8px;
    right: 128px;
  }
  #BK {
    top: 8px;
    left: 168px;
  }

  #RP1 {
    bottom: 128px;
    left: 8px;
  }
  #RP2 {
    bottom: 128px;
    left: 88px;
  }
  #RP3 {
    bottom: 128px;
    left: 168px;
  }
  #RP4 {
    bottom: 128px;
    right: 88px;
  }
  #RP5 {
    bottom: 128px;
    right: 8px;
  }
  #RC1 {
    bottom: 88px;
    left: 48px;
  }
  #RC2 {
    bottom: 88px;
    right: 48px;
  }
  #RR1 {
    bottom: 8px;
    left: 8px;
  }
  #RR2 {
    bottom: 8px;
    right: 8px;
  }
  #RN1 {
    bottom: 8px;
    left: 48px;
  }
  #RN2 {
    bottom: 8px;
    right: 48px;
  }
  #RB1 {
    bottom: 8px;
    left: 88px;
  }
  #RB2 {
    bottom: 8px;
    right: 88px;
  }
  #RA1 {
    bottom: 8px;
    left: 128px;
  }
  #RA2 {
    bottom: 8px;
    right: 128px;
  }
  #RK {
    bottom: 8px;
    left: 168px;
  }
</style>