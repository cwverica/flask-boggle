
class BoggleBoard {

    /**
     * Constructor for game instance
     */
    constructor(name){
        this.board = $('#' + name);
        this.score = 0;
        this.sucesses = [];
        this.failures = [];
        this.seen = new Set();
    }

    /* Called on document ready, starts timer, and submit listener */
    handleStartGame(){
        game.startTimer();
        $('.add-entry').submit(function(evt) {
            evt.preventDefault();
            game.attemptAdd();
        })
    }

    startTimer(){
        let time = 60;
        const interval = setInterval(() => {
            console.log(time);
            $('#timer').text(time);
            if (time > 0){
                time -= 1;
            } else if (time === 0) {
                game.handleEndGame();
                $('#timerLabel').hide();
                clearInterval(interval);
            }
        }, 1000);
    }

    /*Pulls the word from the form, checks it's originality,
        checks the validity of the word, files it accordingly among
        either success or failure*/
    async attemptAdd(){
        const $score = $('#score');
        const $entry = $('#entry');
        let entry = $entry.val();
        

        $entry.val("");
        if (this.seen.has(entry)) {
            window.alert("You've already tried this word. Enter something new")
            $entry.val("");
            return;
        }
        
        this.seen.add(entry);
        const response = await this.checkIsValid(entry);

        if (response.data.result === 'ok') {
            this.sucesses.push(entry);
            this.score += entry.length;
            console.log(this.score);
            $score.text(this.score);
            // refresh successes list
        } else {
            this.failures.push(entry);
            if (response.data.result === 'not-on-board'){
                window.alert("The word you entered is not on the board.")
            } else {
                window.alert("The word you entered is not an english word.")
            }
            // refresh failures list
        }

    
        return
    }
    
    /* Receives the word to be validated, sends a post request to
        the app containing only the word passed in,
        returns a response code */
    async checkIsValid(word){
        try {
            const response = await axios({
                url: `/check-entry`,
                method: `POST`,
                data: {
                  entry: word
                  }
              });
              return response;
        } catch(e) {
            window.alert("/check-entry failed", e)
            return 'failure'
        }
    }

    /* function to end the game. Disables player from submitting any more
        entries, then compares high score and increments play count */
    async endGame(){
        const response = await axios.post("/scores", { score: this.score });
        if (response.data.higherScore) {
          window.alert(`Congratulations! ${this.score} was the high score!`);
        } else {
          window.alert(`Your final score was: ${this.score}`);
        }
      }

    /* event hanlder, calls for the end of the game */
    handleEndGame(){
        $('.add-entry').submit(function(evt) {
            evt.preventDefault();
        });
        $('.add-entry').hide();
        game.endGame();
    }

}

