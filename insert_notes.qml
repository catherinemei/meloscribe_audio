import MuseScore 3.0
import QtQuick 2.9
import FileIO 3.0
import "notes.js" as Notes


MuseScore {
  menuPath: "Plugins.debug7"
  
  //  FileIO {
  //     id: io
  //     source: currentPath() +  "/data_files/twinkle.csv"
  //     onError: console.log("FileIO Error")
  //  }
   
  onRun:{
    // console.log(Notes.notes);
    // console.log(io.source);
    var c=curScore.newCursor();
    c.inputStateMode=Cursor.INPUT_STATE_SYNC_WITH_SCORE
    curScore.startCmd();
    var durationPairs = [];
    const tempo = c.tempo;
    for (var i = 0; i < Notes.notes.length; i++) {
    var note = Notes.notes[i];
      durationPairs.push({duration: Math.floor(( note.end_sec - note.start_sec ) * 16 / tempo)});
    }
    
    for (var i = 0; i < Notes.notes.length; i++) {
    var pair = durationPairs[i];
      c.setDuration(pair.duration , 16);
       c.addNote(64, false); // c.addNote(60,true) to insert note to chord
    }
    
    console.log(c.tempo);
    curScore.endCmd();
  }
}
