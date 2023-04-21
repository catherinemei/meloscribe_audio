import MuseScore 3.0
import QtQuick 2.9
import FileIO 3.0
import QDir 1.0


MuseScore {
  menuPath: "Plugins.debug7"
  
   FileIO {
      id: io
      source: currentPath() +  "/data_files/twinkle.csv"
      onError: console.log("FileIO Error")
   }
   
  onRun:{
  
    console.log(io.source);
    var c=curScore.newCursor();
    c.inputStateMode=Cursor.INPUT_STATE_SYNC_WITH_SCORE
    curScore.startCmd()
    for (var i = 0; i < 10; i++) {
      c.setDuration( 1, 4);
       c.addNote(64, false); // c.addNote(60,true) to insert note to chord
    }
    console.log(c.tempo);
    curScore.endCmd();
  }
}
