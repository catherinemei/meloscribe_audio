import MuseScore 3.0
import QtQuick 2.9
import FileIO 3.0
import "js_files_notes/recording.js" as Notes


MuseScore {
  menuPath: "Plugins.MeloScribe"
  
  //  FileIO {
  //     id: io
  //     source: currentPath() +  "/data_files/twinkle.csv"
  //     onError: console.log("FileIO Error")
  //  }
    QProcess {
    id: proc
  }
      
  

  // Run python script for audio transcribing
  function runCommand(){
      proc.start("pwd");
      proc.waitForFinished(300000);
      console.log(proc.readAllStandardOutput());
      // proc.start("source /Users/20gracehuang/Downloads/Documents/MIT\ Files/2023-spring-classes/6.8510/meloscribe_audio/run_script.sh");
      proc.start("bash", ["-c", "source \"/Users/20gracehuang/Downloads/Documents/MIT\ Files/2023-spring-classes/6.8510/meloscribe_audio/run_script.sh\""]);
      var venv = proc.waitForFinished(-1);
      console.log(venv);
      console.log("Output", proc.readAllStandardOutput());
      // console.log("running command", cmd);
      var args = new Array();
      args[0] = "audio_processing.py";
      // proc.start("file:///Users/20gracehuang/Downloads/Documents/MIT\ Files/2023-spring-classes/6.8510/meloscribe_audio/venv/bin/python3.7 audio_processing.py");
      // var val = proc.waitForFinished(-1);
      // if (val) {
      //    var res = proc.readAllStandardOutput();
      //    console.log(res);
      //    return(res);
      // } else {
      //    console.log("Command failed");
      //    return;
      // }
  }
   
  onRun:{
    // console.log(Notes.notes);
    // console.log(io.source);
    runCommand();
    var c=curScore.newCursor();
    c.inputStateMode=Cursor.INPUT_STATE_SYNC_WITH_SCORE
    curScore.startCmd();
    var durationPairs = [];
    const tempo = c.tempo;
    for (var i = 0; i < Notes.notes.length; i++) {
    var note = Notes.notes[i];
    console.log(note.note_midi);
      durationPairs.push({duration: Math.round(( note.end_sec - note.start_sec ) * 16 / tempo), note: note.note_midi});
    }
    
    for (var i = 0; i < Notes.notes.length; i++) {
    var pair = durationPairs[i];
      c.setDuration(pair.duration , 16);
       c.addNote(pair.note, false); // c.addNote(60,true) to insert note to chord
    }
    
    console.log(c.tempo);
    curScore.endCmd();
  }
}
