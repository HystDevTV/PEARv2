import React, { useState, useEffect, useRef } from 'react';
import { Users, Bot, Play, Send, Eye, EyeOff, Trophy, RotateCcw, Wifi, WifiOff, Copy, UserPlus } from 'lucide-react';

// Firebase Mock - In echter App würde hier Firebase importiert werden
const mockFirebase = {
  database: () => ({
    ref: (path) => ({
      push: (data) => Promise.resolve({ key: 'mock-id-' + Date.now() }),
      set: (data) => Promise.resolve(),
      on: (event, callback) => {
        // Mock listener - würde echte Firebase Events hören
        setTimeout(() => callback({ val: () => null }), 100);
      },
      off: () => {},
      once: (event) => Promise.resolve({ val: () => null })
    })
  })
};

const KalbsleberGame = () => {
  const [gameState, setGameState] = useState('menu'); // menu, online-setup, waiting-room, settings, setup, playing, guessing, results
  const [gameMode, setGameMode] = useState(''); // online, ai
  const [baseWord, setBaseWord] = useState('');
  const [leftLetters, setLeftLetters] = useState([]);
  const [rightLetters, setRightLetters] = useState([]);
  const [wordDisplayCount, setWordDisplayCount] = useState(0);
  const [playerWords, setPlayerWords] = useState([]);
  const [opponentWords, setOpponentWords] = useState([]);
  const [currentWord, setCurrentWord] = useState('');
  const [playerClues, setPlayerClues] = useState([]);
  const [opponentClues, setOpponentClues] = useState([]);
  const [currentClue, setCurrentClue] = useState('');
  const [guessPhase, setGuessPhase] = useState('player');
  const [playerGuesses, setPlayerGuesses] = useState([]);
  const [opponentGuesses, setOpponentGuesses] = useState([]);
  const [scores, setScores] = useState({ player: 0, opponent: 0 });
  const [timeLeft, setTimeLeft] = useState(60);
  const [isTimerActive, setIsTimerActive] = useState(false);
  
  // Online-System States
  const [isOnline, setIsOnline] = useState(false);
  const [roomCode, setRoomCode] = useState('');
  const [playerId, setPlayerId] = useState('');
  const [playerName, setPlayerName] = useState('');
  const [opponentName, setOpponentName] = useState('');
  const [isHost, setIsHost] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('disconnected'); // disconnected, connecting, connected, waiting
  const [roomCodeInput, setRoomCodeInput] = useState('');
  const [playerNameInput, setPlayerNameInput] = useState('');
  const [onlineError, setOnlineError] = useState('');
  
  // Neue Einstellungen - Regelbaukasten
  const [gameSettings, setGameSettings] = useState({
    timeMode: 'total', // 'perWord', 'total', 'unlimited'
    timePerWord: 2, // 1-3 Minuten pro Wort
    totalTime: 12, // 12-15 Minuten für alles
    minWordLength: 3, // Minimale Buchstabenanzahl
    maxWordLength: 8, // Maximale Buchstabenanzahl
    wordDisplayMode: 'permanent', // 'timed', 'permanent', 'onDemand'
    wordDisplayDuration: 3, // Sekunden für timed mode
    showWordCount: 2, // Wie oft das Wort gezeigt wird
    allowHints: true, // Hinweise erlaubt
    maxWordsPerPlayer: 10, // Maximum Wörter pro Spieler
    scoringMode: 'standard' // 'standard', 'length-bonus', 'difficulty-bonus'
  });

  // Neuer State für Wort-Anzeige
  const [wordVisible, setWordVisible] = useState(true);
  const [canToggleWord, setCanToggleWord] = useState(true);

  // Wörterbuch für Wortgenerierung - erweitert mit verschiedenen Längen
  const wordList = {
    3: ['Hund', 'Katze', 'Baum', 'Haus', 'Auto', 'Buch', 'Tisch', 'Stuhl', 'Stern', 'Mond', 'Sonne'],
    4: ['Spiel', 'Blume', 'Wasser', 'Feuer', 'Berg', 'Fluss', 'Meer', 'Wolf', 'Hase', 'Rose'],
    5: ['Garten', 'Fenster', 'Tiger', 'Fuchs', 'Stunde', 'Tasche', 'Seide', 'Eule', 'Lupe'],
    6: ['Computer', 'Kaffee', 'Butter', 'Messer', 'Papier', 'Betten', 'Himmel', 'Wolken'],
    7: ['Schule', 'Familie', 'Freunde', 'Küche', 'Zimmer', 'Garten', 'Reisen', 'Wetter'],
    8: ['Geburtstag', 'Schokolade', 'Telefon', 'Internet', 'Computer', 'Geschenk', 'Freizeit']
  };

  // Timer Effekt
  useEffect(() => {
    let interval = null;
    if (isTimerActive && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft(timeLeft => timeLeft - 1);
      }, 1000);
    } else if (timeLeft === 0) {
      setIsTimerActive(false);
      if (gameState === 'playing') {
        if (gameSettings.timeMode === 'perWord') {
          // Pro Wort Timer - nächstes Wort oder Ende
          setTimeLeft(gameSettings.timePerWord * 60);
        } else {
          // Gesamt Timer - zum Rate-Phase
          setGameState('guessing');
          generateCluesPhase();
        }
      }
    }
    return () => clearInterval(interval);
  }, [isTimerActive, timeLeft, gameState, gameSettings]);

  // Wort Anzeige Effekt - jetzt basierend auf Einstellungen
  useEffect(() => {
    if (gameState === 'setup' && wordDisplayCount < gameSettings.showWordCount) {
      if (gameSettings.wordDisplayMode === 'timed') {
        const timer = setTimeout(() => {
          setWordVisible(false);
          setTimeout(() => {
            setWordVisible(true);
            setWordDisplayCount(prev => prev + 1);
            if (wordDisplayCount === gameSettings.showWordCount - 1) {
              setTimeout(() => {
                setGameState('playing');
                setTimeLeft(gameSettings.timeMode === 'perWord' ? gameSettings.timePerWord * 60 : 
                           gameSettings.timeMode === 'total' ? gameSettings.totalTime * 60 : 999999);
                setIsTimerActive(gameSettings.timeMode !== 'unlimited');
              }, gameSettings.wordDisplayDuration * 1000);
            }
          }, 1000);
        }, gameSettings.wordDisplayDuration * 1000);
        return () => clearTimeout(timer);
      } else if (gameSettings.wordDisplayMode === 'permanent') {
        // Bei permanent mode sofort weiter nach kurzer Pause
        const timer = setTimeout(() => {
          setWordDisplayCount(prev => prev + 1);
          if (wordDisplayCount === gameSettings.showWordCount - 1) {
            setGameState('playing');
            setWordVisible(true); // Wort bleibt sichtbar
            setTimeLeft(gameSettings.timeMode === 'perWord' ? gameSettings.timePerWord * 60 : 
                       gameSettings.timeMode === 'total' ? gameSettings.totalTime * 60 : 999999);
            setIsTimerActive(gameSettings.timeMode !== 'unlimited');
          }
        }, 2000);
        return () => clearTimeout(timer);
      }
    }
  }, [gameState, wordDisplayCount, gameSettings]);

  const generateRandomWord = () => {
    const availableLengths = Object.keys(wordList).filter(length => 
      parseInt(length) >= gameSettings.minWordLength && 
      parseInt(length) <= gameSettings.maxWordLength
    );
    
    if (availableLengths.length === 0) {
      // Fallback auf mittlere Länge
      const length = Math.max(3, Math.min(8, gameSettings.minWordLength));
      const words = wordList[length] || wordList[4];
      const word = words[Math.floor(Math.random() * words.length)];
      setBaseWord(word.toUpperCase());
      setLeftLetters(word.toUpperCase().split(''));
      setRightLetters(word.toUpperCase().split('').reverse());
      return;
    }
    
    const randomLength = availableLengths[Math.floor(Math.random() * availableLengths.length)];
    const words = wordList[randomLength];
    const word = words[Math.floor(Math.random() * words.length)];
    setBaseWord(word.toUpperCase());
    setLeftLetters(word.toUpperCase().split(''));
    setRightLetters(word.toUpperCase().split('').reverse());
  };

  // Online-Funktionen
  const generateRoomCode = () => {
    const prefix = 'KALBS';
    const numbers = Math.floor(1000 + Math.random() * 9000);
    return `${prefix}-${numbers}`;
  };

  const generatePlayerId = () => {
    return 'player_' + Math.random().toString(36).substr(2, 9);
  };

  const createOnlineRoom = async () => {
    try {
      setConnectionStatus('connecting');
      setOnlineError('');
      
      const newRoomCode = generateRoomCode();
      const newPlayerId = generatePlayerId();
      
      // Firebase Raum erstellen
      const roomRef = mockFirebase.database().ref('rooms/' + newRoomCode);
      await roomRef.set({
        host: newPlayerId,
        players: {
          [newPlayerId]: {
            name: playerNameInput || 'Spieler 1',
            isHost: true,
            ready: false
          }
        },
        gameSettings: gameSettings,
        gameState: 'waiting',
        createdAt: Date.now()
      });

      setRoomCode(newRoomCode);
      setPlayerId(newPlayerId);
      setPlayerName(playerNameInput || 'Spieler 1');
      setIsHost(true);
      setConnectionStatus('waiting');
      setGameState('waiting-room');
      
      // Auf zweiten Spieler hören
      listenForOpponent(newRoomCode);
      
    } catch (error) {
      setOnlineError('Raum konnte nicht erstellt werden');
      setConnectionStatus('disconnected');
    }
  };

  const joinOnlineRoom = async () => {
    try {
      setConnectionStatus('connecting');
      setOnlineError('');
      
      if (!roomCodeInput.trim()) {
        setOnlineError('Bitte Raum-Code eingeben');
        return;
      }

      const newPlayerId = generatePlayerId();
      const roomRef = mockFirebase.database().ref('rooms/' + roomCodeInput.toUpperCase());
      
      // Prüfen ob Raum existiert
      const roomSnapshot = await roomRef.once('value');
      const roomData = roomSnapshot.val();
      
      if (!roomData) {
        setOnlineError('Raum nicht gefunden');
        setConnectionStatus('disconnected');
        return;
      }

      if (Object.keys(roomData.players || {}).length >= 2) {
        setOnlineError('Raum ist voll');
        setConnectionStatus('disconnected');
        return;
      }

      // Dem Raum beitreten
      await roomRef.child('players/' + newPlayerId).set({
        name: playerNameInput || 'Spieler 2',
        isHost: false,
        ready: false
      });

      setRoomCode(roomCodeInput.toUpperCase());
      setPlayerId(newPlayerId);
      setPlayerName(playerNameInput || 'Spieler 2');
      setIsHost(false);
      setConnectionStatus('connected');
      setGameState('waiting-room');
      
      // Game Settings vom Host übernehmen
      setGameSettings(roomData.gameSettings || gameSettings);
      
      // Auf Spiel-Updates hören
      listenForGameUpdates(roomCodeInput.toUpperCase());
      
    } catch (error) {
      setOnlineError('Verbindung fehlgeschlagen');
      setConnectionStatus('disconnected');
    }
  };

  const listenForOpponent = (code) => {
    const playersRef = mockFirebase.database().ref('rooms/' + code + '/players');
    playersRef.on('value', (snapshot) => {
      const players = snapshot.val() || {};
      const playerList = Object.values(players);
      
      if (playerList.length === 2) {
        const opponent = playerList.find(p => !p.isHost);
        setOpponentName(opponent?.name || 'Gegner');
        setConnectionStatus('connected');
      }
    });
  };

  const listenForGameUpdates = (code) => {
    const gameRef = mockFirebase.database().ref('rooms/' + code);
    gameRef.on('value', (snapshot) => {
      const roomData = snapshot.val();
      if (roomData) {
        // Sync game state, words, etc.
        // In echter App: Spiel-Synchronisation implementieren
      }
    });
  };

  const leaveOnlineRoom = () => {
    if (roomCode && playerId) {
      const playerRef = mockFirebase.database().ref(`rooms/${roomCode}/players/${playerId}`);
      playerRef.remove();
    }
    
    setIsOnline(false);
    setRoomCode('');
    setPlayerId('');
    setPlayerName('');
    setOpponentName('');
    setIsHost(false);
    setConnectionStatus('disconnected');
    setOnlineError('');
    setGameState('menu');
  };

  const copyRoomCode = () => {
    navigator.clipboard.writeText(roomCode);
    // Feedback geben
  };

  const startOnlineGame = () => {
    if (isHost && connectionStatus === 'connected') {
      // Game Settings an beide Spieler senden
      const gameRef = mockFirebase.database().ref('rooms/' + roomCode);
      gameRef.child('gameState').set('starting');
      gameRef.child('gameSettings').set(gameSettings);
      
      // Zum Setup wechseln
      setGameState('settings');
    }
  };
    setGameMode(mode);
    setGameState('settings');
  };

  const startGameWithSettings = () => {
    generateRandomWord();
    setGameState('setup');
    setWordDisplayCount(0);
    setWordVisible(true);
    setCanToggleWord(gameSettings.wordDisplayMode === 'onDemand');
    resetGameData();
    
    // Online-Synchronisation
    if (gameMode === 'online' && roomCode) {
      syncGameStart();
    }
  };

  const syncGameStart = () => {
    const gameRef = mockFirebase.database().ref('rooms/' + roomCode);
    gameRef.child('currentWord').set(baseWord);
    gameRef.child('gamePhase').set('setup');
    gameRef.child('gameSettings').set(gameSettings);
  };

  const syncPlayerWords = (words) => {
    if (gameMode === 'online' && roomCode && playerId) {
      const playerRef = mockFirebase.database().ref(`rooms/${roomCode}/players/${playerId}`);
      playerRef.child('words').set(words);
    }
  };

  const syncPlayerClues = (clues) => {
    if (gameMode === 'online' && roomCode && playerId) {
      const playerRef = mockFirebase.database().ref(`rooms/${roomCode}/players/${playerId}`);
      playerRef.child('clues').set(clues);
    }
  };

  // Überschreibe addWord für Online-Sync
  const addWord = () => {
    if (currentWord.trim() && isValidWord(currentWord.trim()) && playerWords.length < gameSettings.maxWordsPerPlayer) {
      const newWords = [...playerWords, currentWord.trim().toUpperCase()];
      setPlayerWords(newWords);
      setCurrentWord('');
      
      // Online synchronisieren
      if (gameMode === 'online') {
        syncPlayerWords(newWords);
      }
    }
  };

  // Überschreibe addClue für Online-Sync
  const addClue = () => {
    if (currentClue.trim()) {
      const newClues = [...playerClues, currentClue.trim()];
      setPlayerClues(newClues);
      setCurrentClue('');
      
      // Online synchronisieren
      if (gameMode === 'online') {
        syncPlayerClues(newClues);
      }
    }
  };

  const resetGameData = () => {
    setPlayerWords([]);
    setOpponentWords([]);
    setPlayerClues([]);
    setOpponentClues([]);
    setPlayerGuesses([]);
    setOpponentGuesses([]);
    setScores({ player: 0, opponent: 0 });
    setCurrentWord('');
    setCurrentClue('');
  };

  const addWord = () => {
    if (currentWord.trim() && isValidWord(currentWord.trim()) && playerWords.length < gameSettings.maxWordsPerPlayer) {
      setPlayerWords(prev => [...prev, currentWord.trim().toUpperCase()]);
      setCurrentWord('');
    }
  };

  const isValidWord = (word) => {
    if (word.length < gameSettings.minWordLength || word.length > gameSettings.maxWordLength) {
      return false;
    }
    const firstLetter = word[0].toUpperCase();
    const lastLetter = word[word.length - 1].toUpperCase();
    return leftLetters.includes(firstLetter) && rightLetters.includes(lastLetter);
  };

  const generateCluesPhase = () => {
    // KI-Wörter generieren
    if (gameMode === 'ai') {
      const aiWords = generateAIWords();
      setOpponentWords(aiWords);
    } else if (gameMode === 'online') {
      // Online: Gegner-Wörter aus Firebase laden
      loadOpponentData();
    }
    setGameState('guessing');
  };

  const loadOpponentData = async () => {
    if (roomCode && playerId) {
      try {
        const roomRef = mockFirebase.database().ref('rooms/' + roomCode + '/players');
        const snapshot = await roomRef.once('value');
        const players = snapshot.val() || {};
        
        // Finde Gegner-Daten
        const opponentData = Object.values(players).find(p => 
          Object.keys(players).find(id => players[id] === p) !== playerId
        );
        
        if (opponentData) {
          setOpponentWords(opponentData.words || []);
          setOpponentClues(opponentData.clues || []);
        }
      } catch (error) {
        console.error('Fehler beim Laden der Gegner-Daten:', error);
      }
    }
  };

  const generateAIWords = () => {
    const validWords = [];
    const possibleWords = [
      'HASE', 'ROSE', 'SEIDE', 'EULE', 'LUPE', 'TASCHE', 'ECHO', 'OFEN',
      'NEST', 'TIGER', 'RABE', 'ENTE', 'WOLF', 'FUCHS', 'STUNDE'
    ];
    
    for (let word of possibleWords) {
      if (isValidWord(word) && validWords.length < Math.min(3, gameSettings.maxWordsPerPlayer)) {
        validWords.push(word);
      }
    }
    return validWords;
  };

  const addClue = () => {
    if (currentClue.trim()) {
      setPlayerClues(prev => [...prev, currentClue.trim()]);
      setCurrentClue('');
    }
  };

  const generateAIClues = () => {
    const clues = [];
    opponentWords.forEach(word => {
      const clueOptions = {
        'HASE': 'Springt durch den Garten',
        'ROSE': 'Rote Blume mit Dornen',
        'SEIDE': 'Glänzender Stoff',
        'EULE': 'Nachtaktiver Vogel',
        'LUPE': 'Macht Dinge größer',
        'TASCHE': 'Trägt man bei sich',
        'ECHO': 'Wiederholung von Geräuschen',
        'OFEN': 'Macht Essen warm',
        'NEST': 'Zuhause für Vögel',
        'TIGER': 'Gestreiftes Raubtier',
        'RABE': 'Schwarzer Vogel',
        'ENTE': 'Schwimmt im Teich',
        'WOLF': 'Heult bei Vollmond',
        'FUCHS': 'Schlaues rotes Tier',
        'STUNDE': 'Zeit von 60 Minuten'
      };
      clues.push(clueOptions[word] || 'Schwer zu erraten');
    });
    setOpponentClues(clues);
  };

  const submitGuess = (guess, isPlayer = true) => {
    if (isPlayer) {
      setPlayerGuesses(prev => [...prev, guess]);
    } else {
      setOpponentGuesses(prev => [...prev, guess]);
    }
  };

  const calculateScore = () => {
    let playerScore = 0;
    let opponentScore = 0;

    // Spieler Punkte
    playerGuesses.forEach(guess => {
      if (opponentWords.map(w => w.toLowerCase()).includes(guess.toLowerCase())) {
        playerScore++;
      }
    });

    // Gegner Punkte (KI rät perfekt zu 70%)
    if (gameMode === 'ai') {
      playerWords.forEach(() => {
        if (Math.random() > 0.3) opponentScore++;
      });
    }

    setScores({ player: playerScore, opponent: opponentScore });
    setGameState('results');
  };

  const toggleWordVisibility = () => {
    if (canToggleWord) {
      setWordVisible(!wordVisible);
    }
  };

  const resetGame = () => {
    // Online-Raum verlassen wenn nötig
    if (gameMode === 'online' && roomCode) {
      leaveOnlineRoom();
    } else {
      setGameState('menu');
      resetGameData();
    }
  };

  // Besserer Hintergrund - nicht gelb
  const doodleStyle = {
    fontFamily: "'Comic Sans MS', cursive, sans-serif",
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    minHeight: '100vh'
  };

  const buttonStyle = {
    background: '#fff',
    border: '3px solid #2d3436',
    borderRadius: '15px',
    transform: 'rotate(-1deg)',
    boxShadow: '4px 4px 0px #2d3436',
    transition: 'all 0.1s'
  };

  const cardStyle = {
    background: '#fff',
    border: '3px solid #2d3436',
    borderRadius: '20px',
    transform: 'rotate(1deg)',
    boxShadow: '6px 6px 0px #2d3436'
  };

  return (
    <div style={doodleStyle} className="p-4 min-h-screen">
      {/* Header */}
      <div className="text-center mb-6">
        <h1 className="text-5xl font-bold text-white transform -rotate-2 drop-shadow-lg">
          🐄 KALBSLEBER 🐄
        </h1>
        <p className="text-xl text-white/90 mt-2 transform rotate-1 drop-shadow">
          Das ultimative Wortspiel!
        </p>
      </div>

      {/* Menu Screen */}
      {gameState === 'menu' && (
        <div className="max-w-2xl mx-auto">
          <div style={cardStyle} className="p-8 mb-4">
            <h2 className="text-3xl font-bold mb-6 text-center">Spielmodus wählen</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <button
                onClick={() => startGame('online')}
                style={buttonStyle}
                className="p-6 text-xl font-bold hover:transform hover:rotate-0 hover:scale-105"
              >
                <Users className="mx-auto mb-2" size={48} />
                <div>Online gegen Freund</div>
              </button>
              <button
                onClick={() => startGame('ai')}
                style={buttonStyle}
                className="p-6 text-xl font-bold hover:transform hover:rotate-0 hover:scale-105"
              >
                <Bot className="mx-auto mb-2" size={48} />
                <div>Gegen KI</div>
              </button>
            </div>
          </div>
          
          <div style={cardStyle} className="p-6 transform -rotate-1">
            <h3 className="font-bold mb-4 text-xl">🎮 Spielregeln:</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <ul className="space-y-2">
                <li>• Ein Wort wird angezeigt (links: oben→unten, rechts: unten→oben)</li>
                <li>• Finde Wörter die mit linkem Buchstaben anfangen und rechtem enden</li>
                <li>• Beschreibe deine Wörter mit Hinweisen</li>
              </ul>
              <ul className="space-y-2">
                <li>• Rate die Wörter des Gegners</li>
                <li>• Wer mehr errät, gewinnt!</li>
                <li>• Viele Regeln sind anpassbar!</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Online Setup Screen */}
      {gameState === 'online-setup' && (
        <div className="max-w-2xl mx-auto">
          <div style={cardStyle} className="p-8 mb-4">
            <h2 className="text-3xl font-bold mb-6 text-center">🌐 Online-Spiel</h2>
            
            {/* Spielername eingeben */}
            <div className="mb-6">
              <label className="block font-bold mb-2 text-lg">Dein Name:</label>
              <input
                type="text"
                value={playerNameInput}
                onChange={(e) => setPlayerNameInput(e.target.value)}
                placeholder="Wie heißt du?"
                className="w-full p-4 border-3 border-gray-800 rounded-lg text-lg font-bold"
                maxLength={20}
              />
            </div>

            {/* Verbindungsstatus */}
            <div className="mb-6 text-center">
              <div className="flex items-center justify-center mb-2">
                {connectionStatus === 'connected' ? (
                  <Wifi className="text-green-600 mr-2" size={24} />
                ) : (
                  <WifiOff className="text-gray-400 mr-2" size={24} />
                )}
                <span className="font-bold">
                  Status: {connectionStatus === 'disconnected' ? 'Nicht verbunden' :
                          connectionStatus === 'connecting' ? 'Verbinde...' :
                          connectionStatus === 'waiting' ? 'Warte auf Gegner...' :
                          'Verbunden!'}
                </span>
              </div>
              
              {onlineError && (
                <div className="bg-red-200 p-3 rounded-lg border-2 border-red-600 mb-4">
                  <strong>Fehler:</strong> {onlineError}
                </div>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              {/* Raum erstellen */}
              <div style={cardStyle} className="p-6 transform rotate-1">
                <h3 className="text-xl font-bold mb-4 text-center text-blue-600">
                  Raum erstellen
                </h3>
                <p className="text-sm mb-4 text-gray-600">
                  Erstelle einen neuen Spielraum und teile den Code mit deinem Freund.
                </p>
                <button
                  onClick={createOnlineRoom}
                  disabled={connectionStatus === 'connecting' || !playerNameInput.trim()}
                  style={!playerNameInput.trim() ? 
                    {...buttonStyle, opacity: 0.5} : 
                    {...buttonStyle, background: '#a7f3d0'}}
                  className="w-full p-4 text-lg font-bold hover:scale-105 disabled:hover:scale-100"
                >
                  <UserPlus className="inline mr-2" />
                  Raum erstellen
                </button>
              </div>

              {/* Raum beitreten */}
              <div style={cardStyle} className="p-6 transform -rotate-1">
                <h3 className="text-xl font-bold mb-4 text-center text-green-600">
                  Raum beitreten
                </h3>
                <div className="space-y-3">
                  <input
                    type="text"
                    value={roomCodeInput}
                    onChange={(e) => setRoomCodeInput(e.target.value.toUpperCase())}
                    placeholder="KALBS-1234"
                    className="w-full p-3 border-2 border-gray-800 rounded-lg text-center font-bold text-lg"
                    maxLength={10}
                  />
                  <button
                    onClick={joinOnlineRoom}
                    disabled={connectionStatus === 'connecting' || !roomCodeInput.trim() || !playerNameInput.trim()}
                    style={(!roomCodeInput.trim() || !playerNameInput.trim()) ? 
                      {...buttonStyle, opacity: 0.5} : 
                      {...buttonStyle, background: '#fbbf24'}}
                    className="w-full p-4 text-lg font-bold hover:scale-105 disabled:hover:scale-100"
                  >
                    <Wifi className="inline mr-2" />
                    Beitreten
                  </button>
                </div>
              </div>
            </div>

            {/* Zurück Button */}
            <div className="mt-6 text-center">
              <button
                onClick={() => setGameState('menu')}
                style={buttonStyle}
                className="px-8 py-3 font-bold hover:scale-105"
              >
                ← Zurück zum Menü
              </button>
            </div>
          </div>

          {/* Info Box */}
          <div style={cardStyle} className="p-4 transform rotate-1">
            <h3 className="font-bold mb-2">ℹ️ So funktioniert's:</h3>
            <ul className="text-sm space-y-1">
              <li>• <strong>Raum erstellen:</strong> Du bekommst einen Code zum Teilen</li>
              <li>• <strong>Raum beitreten:</strong> Code vom Freund eingeben</li>
              <li>• <strong>Online spielen:</strong> Alle Aktionen werden synchronisiert</li>
              <li>• <strong>Keine App nötig:</strong> Funktioniert im Browser</li>
            </ul>
          </div>
        </div>
      )}

      {/* Waiting Room */}
      {gameState === 'waiting-room' && (
        <div className="max-w-2xl mx-auto">
          <div style={cardStyle} className="p-8 text-center">
            <h2 className="text-3xl font-bold mb-6">
              {isHost ? '🎯 Warte auf Gegner' : '🎮 Bereit zum Spielen!'}
            </h2>
            
            {/* Raum Info */}
            <div style={cardStyle} className="p-6 mb-6 transform rotate-1">
              <h3 className="text-xl font-bold mb-4">Raum-Code:</h3>
              <div className="flex items-center justify-center space-x-3">
                <span className="text-3xl font-mono bg-yellow-200 px-4 py-2 rounded-lg border-2 border-gray-800">
                  {roomCode}
                </span>
                <button
                  onClick={copyRoomCode}
                  style={buttonStyle}
                  className="p-3 hover:scale-105"
                  title="Code kopieren"
                >
                  <Copy size={20} />
                </button>
              </div>
              {isHost && (
                <p className="text-sm mt-3 text-gray-600">
                  Teile diesen Code mit deinem Freund!
                </p>
              )}
            </div>

            {/* Spieler Status */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div style={cardStyle} className="p-4 transform -rotate-1">
                <h4 className="font-bold text-blue-600">{isHost ? '👑 Du (Host)' : '🎮 Du'}</h4>
                <p className="text-lg">{playerName}</p>
                <div className="text-green-600 font-bold">✅ Bereit</div>
              </div>
              
              <div style={cardStyle} className="p-4 transform rotate-1">
                <h4 className="font-bold text-red-600">
                  {connectionStatus === 'connected' ? '🎯 Gegner' : '⏳ Wartet...'}
                </h4>
                <p className="text-lg">
                  {opponentName || 'Noch nicht verbunden'}
                </p>
                <div className={connectionStatus === 'connected' ? 'text-green-600 font-bold' : 'text-gray-500'}>
                  {connectionStatus === 'connected' ? '✅ Bereit' : '⏳ Wartet...'}
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="space-y-4">
              {isHost && connectionStatus === 'connected' && (
                <button
                  onClick={startOnlineGame}
                  style={{...buttonStyle, background: '#10b981'}}
                  className="w-full p-4 text-xl font-bold hover:scale-105"
                >
                  <Play className="inline mr-2" />
                  Spiel starten!
                </button>
              )}
              
              {!isHost && connectionStatus === 'connected' && (
                <div className="bg-blue-100 p-4 rounded-lg border-2 border-blue-600">
                  <p className="font-bold">Warte auf den Host...</p>
                  <p className="text-sm">Der Host startet das Spiel, wenn alle bereit sind.</p>
                </div>
              )}

              <button
                onClick={leaveOnlineRoom}
                style={buttonStyle}
                className="w-full p-3 font-bold hover:scale-105"
              >
                🚪 Raum verlassen
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Settings Screen - Regelbaukasten */}
      {gameState === 'settings' && (
        <div className="max-w-4xl mx-auto">
          <div style={cardStyle} className="p-8 mb-4">
            <h2 className="text-3xl font-bold mb-6 text-center">🔧 Regelbaukasten</h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              
              {/* Linke Spalte */}
              <div className="space-y-6">
                
                {/* Zeit-Modus */}
                <div>
                  <h3 className="font-bold mb-4 text-xl text-blue-600">⏰ Zeit-Regeln:</h3>
                  <div className="space-y-3">
                    <label className="flex items-center p-4 bg-yellow-100 rounded-lg transform rotate-1 cursor-pointer">
                      <input
                        type="radio"
                        name="timeMode"
                        value="unlimited"
                        checked={gameSettings.timeMode === 'unlimited'}
                        onChange={(e) => setGameSettings(prev => ({...prev, timeMode: e.target.value}))}
                        className="mr-3 scale-150"
                      />
                      <div>
                        <div className="font-bold">Unbegrenzt</div>
                        <div className="text-sm">Keine Zeitbegrenzung</div>
                      </div>
                    </label>
                    
                    <label className="flex items-center p-4 bg-blue-100 rounded-lg transform -rotate-1 cursor-pointer">
                      <input
                        type="radio"
                        name="timeMode"
                        value="total"
                        checked={gameSettings.timeMode === 'total'}
                        onChange={(e) => setGameSettings(prev => ({...prev, timeMode: e.target.value}))}
                        className="mr-3 scale-150"
                      />
                      <div>
                        <div className="font-bold">Gesamt-Zeit</div>
                        <div className="text-sm">Zeit für alle Wörter</div>
                      </div>
                    </label>
                    
                    <label className="flex items-center p-4 bg-green-100 rounded-lg transform rotate-1 cursor-pointer">
                      <input
                        type="radio"
                        name="timeMode"
                        value="perWord"
                        checked={gameSettings.timeMode === 'perWord'}
                        onChange={(e) => setGameSettings(prev => ({...prev, timeMode: e.target.value}))}
                        className="mr-3 scale-150"
                      />
                      <div>
                        <div className="font-bold">Pro Wort</div>
                        <div className="text-sm">Zeit je Wort</div>
                      </div>
                    </label>
                  </div>

                  {/* Zeit-Einstellung */}
                  {gameSettings.timeMode === 'perWord' && (
                    <div className="mt-4">
                      <h4 className="font-bold mb-2">Minuten pro Wort:</h4>
                      <div className="flex space-x-2">
                        {[1, 2, 3].map(minutes => (
                          <button
                            key={minutes}
                            onClick={() => setGameSettings(prev => ({...prev, timePerWord: minutes}))}
                            style={gameSettings.timePerWord === minutes ? 
                              {...buttonStyle, background: '#a7f3d0'} : buttonStyle}
                            className="flex-1 p-3 font-bold hover:scale-105"
                          >
                            {minutes}min
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {gameSettings.timeMode === 'total' && (
                    <div className="mt-4">
                      <h4 className="font-bold mb-2">Gesamt-Zeit:</h4>
                      <div className="flex space-x-2">
                        {[10, 12, 15, 20].map(minutes => (
                          <button
                            key={minutes}
                            onClick={() => setGameSettings(prev => ({...prev, totalTime: minutes}))}
                            style={gameSettings.totalTime === minutes ? 
                              {...buttonStyle, background: '#a7f3d0'} : buttonStyle}
                            className="flex-1 p-2 font-bold text-sm hover:scale-105"
                          >
                            {minutes}min
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Wort-Anzeige */}
                <div>
                  <h3 className="font-bold mb-4 text-xl text-green-600">👁️ Wort-Anzeige:</h3>
                  <div className="space-y-3">
                    <label className="flex items-center p-4 bg-pink-100 rounded-lg transform -rotate-1 cursor-pointer">
                      <input
                        type="radio"
                        name="wordDisplayMode"
                        value="permanent"
                        checked={gameSettings.wordDisplayMode === 'permanent'}
                        onChange={(e) => setGameSettings(prev => ({...prev, wordDisplayMode: e.target.value}))}
                        className="mr-3 scale-150"
                      />
                      <div>
                        <div className="font-bold">Permanent sichtbar</div>
                        <div className="text-sm">Wort bleibt immer da</div>
                      </div>
                    </label>
                    
                    <label className="flex items-center p-4 bg-orange-100 rounded-lg transform rotate-1 cursor-pointer">
                      <input
                        type="radio"
                        name="wordDisplayMode"
                        value="timed"
                        checked={gameSettings.wordDisplayMode === 'timed'}
                        onChange={(e) => setGameSettings(prev => ({...prev, wordDisplayMode: e.target.value}))}
                        className="mr-3 scale-150"
                      />
                      <div>
                        <div className="font-bold">Zeitgesteuert</div>
                        <div className="text-sm">Erscheint & verschwindet</div>
                      </div>
                    </label>
                    
                    <label className="flex items-center p-4 bg-purple-100 rounded-lg transform -rotate-1 cursor-pointer">
                      <input
                        type="radio"
                        name="wordDisplayMode"
                        value="onDemand"
                        checked={gameSettings.wordDisplayMode === 'onDemand'}
                        onChange={(e) => setGameSettings(prev => ({...prev, wordDisplayMode: e.target.value}))}
                        className="mr-3 scale-150"
                      />
                      <div>
                        <div className="font-bold">Auf Knopfdruck</div>
                        <div className="text-sm">Ein-/Ausblenden möglich</div>
                      </div>
                    </label>
                  </div>

                  {gameSettings.wordDisplayMode === 'timed' && (
                    <div className="mt-4">
                      <h4 className="font-bold mb-2">Anzeigedauer: {gameSettings.wordDisplayDuration}s</h4>
                      <input
                        type="range"
                        min="2"
                        max="10"
                        value={gameSettings.wordDisplayDuration}
                        onChange={(e) => setGameSettings(prev => ({...prev, wordDisplayDuration: parseInt(e.target.value)}))}
                        className="w-full h-3 bg-orange-300 rounded-lg appearance-none cursor-pointer"
                      />
                    </div>
                  )}
                </div>
              </div>

              {/* Rechte Spalte */}
              <div className="space-y-6">
                
                {/* Wortlänge */}
                <div>
                  <h3 className="font-bold mb-4 text-xl text-purple-600">📝 Wort-Regeln:</h3>
                  
                  <div className="mb-4">
                    <label className="block font-bold mb-2">Minimum: {gameSettings.minWordLength} Buchstaben</label>
                    <input
                      type="range"
                      min="3"
                      max="6"
                      value={gameSettings.minWordLength}
                      onChange={(e) => setGameSettings(prev => ({
                        ...prev, 
                        minWordLength: parseInt(e.target.value),
                        maxWordLength: Math.max(parseInt(e.target.value), prev.maxWordLength)
                      }))}
                      className="w-full h-3 bg-yellow-300 rounded-lg appearance-none cursor-pointer"
                    />
                  </div>

                  <div className="mb-4">
                    <label className="block font-bold mb-2">Maximum: {gameSettings.maxWordLength} Buchstaben</label>
                    <input
                      type="range"
                      min="4"
                      max="10"
                      value={gameSettings.maxWordLength}
                      onChange={(e) => setGameSettings(prev => ({
                        ...prev, 
                        maxWordLength: parseInt(e.target.value),
                        minWordLength: Math.min(prev.minWordLength, parseInt(e.target.value))
                      }))}
                      className="w-full h-3 bg-blue-300 rounded-lg appearance-none cursor-pointer"
                    />
                  </div>

                  <div className="mb-4">
                    <label className="block font-bold mb-2">Max. Wörter pro Spieler: {gameSettings.maxWordsPerPlayer}</label>
                    <input
                      type="range"
                      min="3"
                      max="20"
                      value={gameSettings.maxWordsPerPlayer}
                      onChange={(e) => setGameSettings(prev => ({...prev, maxWordsPerPlayer: parseInt(e.target.value)}))}
                      className="w-full h-3 bg-green-300 rounded-lg appearance-none cursor-pointer"
                    />
                  </div>

                  <div className="text-center p-3 bg-green-100 rounded-lg font-bold">
                    Wörter: {gameSettings.minWordLength}-{gameSettings.maxWordLength} Buchstaben
                    <br />
                    Max: {gameSettings.maxWordsPerPlayer} Wörter
                  </div>
                </div>

                {/* Spielmodi */}
                <div>
                  <h3 className="font-bold mb-4 text-xl text-red-600">🎯 Spiel-Modi:</h3>
                  
                  <div className="mb-4">
                    <label className="flex items-center p-3 bg-blue-100 rounded-lg">
                      <input
                        type="checkbox"
                        checked={gameSettings.allowHints}
                        onChange={(e) => setGameSettings(prev => ({...prev, allowHints: e.target.checked}))}
                        className="mr-3 scale-150"
                      />
                      <div>
                        <div className="font-bold">Hinweise erlaubt</div>
                        <div className="text-sm">Spieler können Wörter beschreiben</div>
                      </div>
                    </label>
                  </div>

                  <div>
                    <h4 className="font-bold mb-2">Punktesystem:</h4>
                    <select
                      value={gameSettings.scoringMode}
                      onChange={(e) => setGameSettings(prev => ({...prev, scoringMode: e.target.value}))}
                      className="w-full p-3 border-3 border-gray-800 rounded-lg font-bold"
                    >
                      <option value="standard">Standard (1 Punkt pro Treffer)</option>
                      <option value="length-bonus">Längen-Bonus (mehr Punkte für längere Wörter)</option>
                      <option value="difficulty-bonus">Schwierigkeits-Bonus (seltene Wörter = mehr Punkte)</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex space-x-4 mt-8">
              <button
                onClick={() => setGameState('menu')}
                style={buttonStyle}
                className="flex-1 p-4 text-lg font-bold hover:scale-105"
              >
                ← Zurück
              </button>
              <button
                onClick={startGameWithSettings}
                style={{...buttonStyle, background: '#a7f3d0'}}
                className="flex-1 p-4 text-lg font-bold hover:scale-105"
              >
                <Play className="inline mr-2" />
                Spiel starten!
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Setup/Word Display */}
      {gameState === 'setup' && (
        <div className="max-w-2xl mx-auto text-center">
          <div style={cardStyle} className="p-8">
            <h2 className="text-2xl mb-6">Merke dir das Wort!</h2>
            <div className="text-6xl font-bold mb-4">
              Anzeige {wordDisplayCount + 1}/{gameSettings.showWordCount}
            </div>
            
            <div className="mb-6 text-sm bg-white/80 p-3 rounded-lg">
              Wortlänge: {gameSettings.minWordLength}-{gameSettings.maxWordLength} Buchstaben • 
              Zeit: {gameSettings.timeMode === 'perWord' ? 
                `${gameSettings.timePerWord}min pro Wort` : 
                gameSettings.timeMode === 'total' ? 
                `${gameSettings.totalTime}min gesamt` : 
                'Unbegrenzt'} • 
              Anzeige: {gameSettings.wordDisplayMode === 'permanent' ? 'Permanent' : 
                       gameSettings.wordDisplayMode === 'timed' ? `${gameSettings.wordDisplayDuration}s` : 
                       'Auf Knopfdruck'}
            </div>
            
            {(wordVisible || gameSettings.wordDisplayMode === 'permanent') && (
              <div className="flex justify-between items-center h-80 bg-white/10 rounded-lg p-6">
                {/* Linke Seite - von oben nach unten */}
                <div className="flex flex-col text-6xl font-bold text-blue-300 drop-shadow-lg">
                  <div className="text-lg mb-4 text-white">START ↓</div>
                  {leftLetters.map((letter, index) => (
                    <div key={`left-${index}`} className="mb-3 transform rotate-12 hover:scale-110 transition-transform">
                      {letter}
                    </div>
                  ))}
                </div>
                
                {/* Mitte */}
                <div className="text-center text-white/70">
                  <div className="text-4xl mb-4">⚡</div>
                  <div className="font-bold">KALBSLEBER</div>
                </div>
                
                {/* Rechte Seite - von unten nach oben */}
                <div className="flex flex-col-reverse text-6xl font-bold text-pink-300 drop-shadow-lg">
                  <div className="text-lg mt-4 text-white">↑ ENDE</div>
                  {rightLetters.map((letter, index) => (
                    <div key={`right-${index}`} className="mb-3 transform -rotate-12 hover:scale-110 transition-transform">
                      {letter}
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            {!wordVisible && gameSettings.wordDisplayMode !== 'permanent' && (
              <div className="h-80 flex items-center justify-center bg-white/10 rounded-lg">
                <div className="text-4xl text-white/50">Wort versteckt...</div>
              </div>
            )}

            {gameSettings.wordDisplayMode === 'onDemand' && gameState === 'setup' && (
              <button
                onClick={toggleWordVisibility}
                style={buttonStyle}
                className="mt-4 px-6 py-3 font-bold hover:scale-105"
              >
                {wordVisible ? <EyeOff className="inline mr-2" /> : <Eye className="inline mr-2" />}
                {wordVisible ? 'Wort verstecken' : 'Wort anzeigen'}
              </button>
            )}
          </div>
        </div>
      )}

      {/* Playing Phase */}
      {gameState === 'playing' && (
        <div className="max-w-3xl mx-auto">
          <div style={cardStyle} className="p-6 mb-4">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Finde Wörter!</h2>
              <div className="text-right">
                {gameSettings.timeMode !== 'unlimited' && (
                  <div className="text-3xl font-bold text-red-600 mb-2">
                    ⏰ {Math.floor(timeLeft / 60)}:{(timeLeft % 60).toString().padStart(2, '0')}
                  </div>
                )}
                <div className="text-lg">
                  {playerWords.length} / {gameSettings.maxWordsPerPlayer} Wörter
                </div>
              </div>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              
              {/* Linke Spalte - Wort-Referenz und Eingabe */}
              <div className="space-y-4">
                
                {/* Wort-Referenz */}
                {(gameSettings.wordDisplayMode === 'permanent' || 
                  (gameSettings.wordDisplayMode === 'onDemand' && wordVisible)) && (
                  <div style={cardStyle} className="p-4 transform rotate-1">
                    <h3 className="font-bold mb-2 text-center">Referenz-Wort:</h3>
                    <div className="flex justify-between text-2xl font-bold">
                      <div className="text-blue-600">
                        Start: {leftLetters.join(' ')}
                      </div>
                      <div className="text-pink-600">
                        Ende: {rightLetters.join(' ')}
                      </div>
                    </div>
                  </div>
                )}
                
                {gameSettings.wordDisplayMode === 'onDemand' && (
                  <button
                    onClick={toggleWordVisibility}
                    style={buttonStyle}
                    className="w-full p-3 font-bold hover:scale-105"
                  >
                    {wordVisible ? <EyeOff className="inline mr-2" /> : <Eye className="inline mr-2" />}
                    {wordVisible ? 'Wort verstecken' : 'Wort anzeigen'}
                  </button>
                )}

                <div className="text-sm bg-white/20 p-3 rounded-lg text-white">
                  <strong>Regeln:</strong> Wörter müssen {gameSettings.minWordLength}-{gameSettings.maxWordLength} Buchstaben haben
                  und mit einem Start-Buchstaben anfangen sowie mit einem End-Buchstaben aufhören.
                </div>

                <div className="space-y-3">
                  <input
                    type="text"
                    value={currentWord}
                    onChange={(e) => setCurrentWord(e.target.value.toUpperCase())}
                    onKeyPress={(e) => e.key === 'Enter' && addWord()}
                    placeholder={`Wort (${gameSettings.minWordLength}-${gameSettings.maxWordLength} Buchstaben)...`}
                    className="w-full p-4 border-3 border-gray-800 rounded-lg text-xl font-bold"
                    style={{transform: 'rotate(-0.5deg)'}}
                    disabled={playerWords.length >= gameSettings.maxWordsPerPlayer}
                  />
                  <button
                    onClick={addWord}
                    style={buttonStyle}
                    className="w-full p-3 font-bold hover:scale-105"
                    disabled={playerWords.length >= gameSettings.maxWordsPerPlayer}
                  >
                    <Send className="inline mr-2" />
                    Wort hinzufügen
                  </button>
                </div>
              </div>

              {/* Rechte Spalte - Wort-Liste */}
              <div>
                <div style={cardStyle} className="p-4 transform -rotate-1 h-96 overflow-y-auto">
                  <h3 className="font-bold mb-3 text-lg">Deine Wörter ({playerWords.length}):</h3>
                  <div className="space-y-2">
                    {playerWords.map((word, index) => (
                      <div key={index} className="bg-gradient-to-r from-green-200 to-green-300 p-3 rounded-lg font-bold transform rotate-1 hover:scale-105 transition-transform">
                        <div className="flex justify-between items-center">
                          <span className="text-lg">{word}</span>
                          <span className="text-sm bg-white px-2 py-1 rounded">
                            {word.length} Buchstaben
                          </span>
                        </div>
                      </div>
                    ))}
                    
                    {playerWords.length === 0 && (
                      <div className="text-center text-gray-500 py-8">
                        Noch keine Wörter gefunden...
                        <br />
                        <small>Finde Wörter mit den Start- und End-Buchstaben!</small>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {(gameSettings.timeMode === 'unlimited' || timeLeft === 0) && playerWords.length > 0 && (
              <div className="mt-6 text-center">
                <button
                  onClick={() => {
                    setGameState('guessing');
                    generateCluesPhase();
                  }}
                  style={{...buttonStyle, background: '#fbbf24'}}
                  className="px-8 py-4 text-xl font-bold hover:scale-105"
                >
                  <Play className="inline mr-2" />
                  Weiter zur Rate-Phase!
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Guessing Phase */}
      {gameState === 'guessing' && (
        <div className="max-w-4xl mx-auto">
          <div style={cardStyle} className="p-6 mb-4">
            <h2 className="text-2xl font-bold mb-6 text-center">🔍 Rate-Phase!</h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              
              {/* Linke Spalte - Hinweise schreiben */}
              <div>
                <h3 className="font-bold mb-4 text-xl text-blue-600">Schreibe Hinweise für deine Wörter:</h3>
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {playerWords.map((word, index) => (
                    <div key={index} className="p-4 bg-blue-100 rounded-lg transform rotate-1">
                      <div className="font-bold mb-3 text-lg">Wort: {word}</div>
                      {playerClues[index] ? (
                        <div className="bg-green-200 p-3 rounded-lg">
                          <strong>Hinweis:</strong> {playerClues[index]}
                        </div>
                      ) : gameSettings.allowHints ? (
                        <div>
                          <input
                            type="text"
                            value={currentClue}
                            onChange={(e) => setCurrentClue(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && addClue()}
                            placeholder="Beschreibe dieses Wort..."
                            className="w-full p-3 border-2 border-gray-800 rounded-lg mb-2"
                          />
                          <button
                            onClick={addClue}
                            style={buttonStyle}
                            className="px-4 py-2 text-sm hover:scale-105"
                          >
                            Hinweis speichern
                          </button>
                        </div>
                      ) : (
                        <div className="bg-gray-200 p-3 rounded-lg text-center">
                          <em>Hinweise sind deaktiviert</em>
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                {(playerClues.length === playerWords.length || !gameSettings.allowHints) && playerWords.length > 0 && (
                  <div className="mt-6">
                    <button
                      onClick={() => {
                        generateAIClues();
                        setGuessPhase('opponent');
                      }}
                      style={{...buttonStyle, background: '#fbbf24'}}
                      className="w-full p-4 text-lg font-bold hover:scale-105"
                    >
                      <Play className="inline mr-2" />
                      Weiter zum Raten!
                    </button>
                  </div>
                )}
              </div>

              {/* Rechte Spalte - Gegner Wörter raten */}
              {guessPhase === 'opponent' && (
                <div>
                  <h3 className="font-bold mb-4 text-xl text-red-600">Rate die Wörter des Gegners:</h3>
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {opponentClues.map((clue, index) => (
                      <div key={index} className="p-4 bg-yellow-100 rounded-lg transform -rotate-1">
                        <div className="mb-3">
                          <strong>Hinweis:</strong> {clue}
                        </div>
                        <input
                          type="text"
                          placeholder="Deine Vermutung..."
                          onKeyPress={(e) => {
                            if (e.key === 'Enter') {
                              submitGuess(e.target.value);
                              e.target.value = '';
                            }
                          }}
                          className="w-full p-3 border-2 border-gray-800 rounded-lg"
                        />
                      </div>
                    ))}
                  </div>
                  
                  <button
                    onClick={calculateScore}
                    style={{...buttonStyle, background: '#10b981'}}
                    className="w-full mt-6 p-4 text-lg font-bold hover:scale-105"
                  >
                    <Trophy className="inline mr-2" />
                    Ergebnis anzeigen!
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {gameState === 'results' && (
        <div className="max-w-3xl mx-auto">
          <div style={cardStyle} className="p-8 text-center">
            <h2 className="text-4xl font-bold mb-6">
              {scores.player > scores.opponent ? '🎉 Du gewinnst! 🎉' : 
               scores.player < scores.opponent ? '😢 Du verlierst!' : 
               '🤝 Unentschieden!'}
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-6">
              
              {/* Punkte */}
              <div style={cardStyle} className="p-6 transform rotate-1">
                <h3 className="text-2xl font-bold mb-4">Punktestand</h3>
                <div className="text-3xl space-y-2">
                  <div className="flex justify-between">
                    <span>Du:</span>
                    <strong className="text-green-600">{scores.player}</strong>
                  </div>
                  <div className="flex justify-between">
                    <span>Gegner:</span>
                    <strong className="text-red-600">{scores.opponent}</strong>
                  </div>
                </div>
              </div>

              {/* Statistiken */}
              <div style={cardStyle} className="p-6 transform -rotate-1">
                <h3 className="text-2xl font-bold mb-4">Statistiken</h3>
                <div className="text-sm space-y-2">
                  <div>Deine Wörter: <strong>{playerWords.length}</strong></div>
                  <div>Gegner Wörter: <strong>{opponentWords.length}</strong></div>
                  <div>Verwendete Zeit: <strong>
                    {gameSettings.timeMode === 'unlimited' ? 'Unbegrenzt' : 
                     gameSettings.timeMode === 'total' ? `${gameSettings.totalTime - Math.floor(timeLeft / 60)}min` :
                     'Variable'}
                  </strong></div>
                  <div>Punktesystem: <strong>{gameSettings.scoringMode}</strong></div>
                </div>
              </div>
            </div>

            {/* Auflösung */}
            <div className="mb-6">
              <h3 className="font-bold mb-4 text-xl">🔍 Die Auflösung:</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
                <div style={cardStyle} className="p-4 transform rotate-1">
                  <strong className="text-blue-600">Deine Wörter:</strong>
                  <div className="mt-2 space-y-1">
                    {playerWords.map((word, index) => (
                      <div key={index} className="bg-blue-100 p-2 rounded">
                        {word} {gameSettings.allowHints && playerClues[index] && 
                         <span className="text-sm">- {playerClues[index]}</span>}
                      </div>
                    ))}
                  </div>
                </div>
                
                <div style={cardStyle} className="p-4 transform -rotate-1">
                  <strong className="text-red-600">Gegner Wörter:</strong>
                  <div className="mt-2 space-y-1">
                    {opponentWords.map((word, index) => (
                      <div key={index} className="bg-red-100 p-2 rounded">
                        {word} {gameSettings.allowHints && opponentClues[index] && 
                         <span className="text-sm">- {opponentClues[index]}</span>}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <div className="flex space-x-4">
              <button
                onClick={resetGame}
                style={buttonStyle}
                className="flex-1 p-4 text-lg font-bold hover:scale-105"
              >
                <RotateCcw className="inline mr-2" />
                Nochmal spielen!
              </button>
              <button
                onClick={() => setGameState('settings')}
                style={buttonStyle}
                className="flex-1 p-4 text-lg font-bold hover:scale-105"
              >
                ⚙️ Regeln ändern
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default KalbsleberGame;