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
  FileIO {
    id: file
    source: '/Users/20gracehuang/Downloads/Documents/MIT\ Files/2023-spring-classes/6.8510/meloscribe_audio/notes_summary_csv/recording.csv'
  }



  // Run python script for audio transcribing
  function runCommand()
  {
    
    proc.start('/bin/sh -c "/User/20gracehuang/Downloads/Documents/MIT\ Files/2023-spring-classes/6.8510/meloscribe_audio/run_script.sh"');
    // proc.start('bash -c ls');
    var venv = proc.waitForFinished(10000);
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

  onRun: {
    // console.log(Notes.notes);
    // console.log(io.source);
    var notes_new = file.read().split(/\r?\n/).slice(1);
    while(notes_new[notes_new.length - 1] === '') {  // remove any extra blank lines
      notes_new.pop();
    }

    // todo: Figure out how to make this work
   runCommand();
    var c=curScore.newCursor();
    c.inputStateMode=Cursor.INPUT_STATE_SYNC_WITH_SCORE
    curScore.startCmd();
    var durationPairs = [];
    const tempo = c.tempo;
    console.log("tempo", tempo);

    // // doesn't work b/c  javascript file doesn't get updated
    // for (var i = 0; i < Notes.notes.length; i++) {
    //      var note = Notes.notes[i];
    //      console.log(note.note_midi);
    //      durationPairs.push({duration: Math.round(( note.end_sec - note.start_sec ) * 16 / tempo), note: note.note_midi});
    // }

    for (var i = 0; i < notes_new.length; i++) {
      var note = notes_new[i].split(",");
      // TODO: create actual javascript object here
      console.log("current note", note[1], note[2], note[5]);
      console.log("duration", Math.round(( note[2] - note[1] ) * 4 * tempo));
      durationPairs.push({duration: Math.round(( note[2] - note[1] ) * 4 * tempo), note: note[5]});
    }
    console.log(durationPairs);

    for (var i = 0; i < durationPairs.length; i++) {
      var pair = durationPairs[i];
      if(pair.duration !== 0)
      {
            
            c.setDuration(pair.duration, 16);
            if(pair.note > 40)
            // limit to higher octaves for now so that we don't get weird outliers, 
            // change later once we have better handling
                  c.addNote(pair.note, false); // c.addNote(60, true) to insert note to chord
            else {
                  c.addRest();
            }
      }
          
    }

    console.log(c.tempo);
    curScore.endCmd();
  }
}
