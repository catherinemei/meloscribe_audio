import MuseScore 3.0
import QtQuick 2.9
import FileIO 3.0


MuseScore {
  menuPath: "Plugins.MeloScribe"

  QProcess {
    id: proc
  }
  
  FileIO {
    id: file

   
  }

  // In an ideal scenario, we would run the relevant python script for audio transcribing
  // This might work for UNIX, but mac has refused to cooperate. This is kept
  // as a proof of contept, however.
  function runCommand(pathToMeloscribe)
  {
    
    proc.start('/bin/sh -c "'+pathToMeloscribe + 'run_script.sh"');
    var venv = proc.waitForFinished(10000);
    console.log(venv);
    console.log("Output", proc.readAllStandardOutput());
    return proc.readAllStandardOutput();
  }

  onRun: {
    // path to the audio file
    var pathToMeloscribe = '/Users/20gracehuang/Downloads/Documents/MIT\ Files/2023-spring-classes/6.8510/meloscribe_audio';
    file.source = pathToMeloscribe + '/notes_summary_csv/recording.csv';
    var notes_new = file.read().split(/\r?\n/).slice(1);
    while(notes_new[notes_new.length - 1] === '') {  // remove any extra blank lines
      notes_new.pop();
    }
    

    // runCommand();
    var c=curScore.newCursor();
    c.inputStateMode=Cursor.INPUT_STATE_SYNC_WITH_SCORE
    curScore.startCmd();
    var durationPairs = [];
    const tempo = c.tempo;

    // create duration and note pairings
    for (var i = 0; i < notes_new.length; i++) {
      var note = notes_new[i].split(",");
      durationPairs.push({duration: Math.round(( note[2] - note[1] ) * 4 * tempo), note: note[5]});
    }

    for (var i = 0; i < durationPairs.length; i++) {
      var pair = durationPairs[i];
      if(pair.duration !== 0)
      {
            // add if non-zero duration
            c.setDuration(pair.duration, 16);
            if(pair.note > 0) // add note if the note is nonzero (indicating a rest)
                  c.addNote(pair.note, false); 
            else {
                  c.addRest();
            }
      }
          
    }

    curScore.endCmd();
    Qt.quit();
  }
}
