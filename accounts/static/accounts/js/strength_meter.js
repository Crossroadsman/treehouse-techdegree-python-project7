// elements
const passwordField = document.getElementById("id_password1")
const strengthMeter = document.getElementById("strength-meter")
const meterBody = document.getElementById("meter-body")

// password settings
const targetCharacters = 14;
const targetNumbers = 1;
const targetUppers = 1;
const targetSpecials = 1;

// event listeners
passwordField.addEventListener('keyup', () => {
  updateStrengthMeter();     
});

function chooseColour(strength) {

  let colour;
  switch (strength) {
    case 0:
    case 1:
    case 2:
      colour = "#C0392B";
      break;
    case 3:
    case 4:
      colour = "#E74C3C";
      break;
    case 5:
    case 6:
      colour = "#E67E22";
      break;
    case 7:
    case 8:
      colour = "#F1C40F";
      break;
    case 9:
      colour = "#CFED0C";
      break;
    default:
      colour = "#2ECC71"
  }
  return colour;
}

function updateStrengthMeter() {
  // make meter visible
  strengthMeter.style.display = "block";

  const strength = computeStrength(passwordField.value);
  
  let shortStrength = Math.floor(strength / 10);
  if (shortStrength > 10) { 
    shortStrength = 10;
  }
  

  const colour = chooseColour(shortStrength);
  
  const meter =  "█".repeat(shortStrength) + "░".repeat(10 - shortStrength);
  meterBody.style.fontFamily = "monospace";
  meterBody.style.color = colour;
  meterBody.textContent = meter;
}

function computeStrength(str) {
  // define relative weighting of length vs other factors
  const lengthMaxPoints = 50;
  const otherMaxPoints = 50;

  let length = str.length;
  let numbers = 0
  let uppers = 0;
  let specials = 0;

  if (length < 1) {
    return 0;
  }

  for (let i = 0; i < length; i++) {
    if (isUpper(str[i])) {
      uppers++;
    } else if (isNumber(str[i])) {
      numbers++;
    } else if (isSpecial(str[i])) {
      specials++;
    }

  }

  if (length > targetCharacters) {
    length = targetCharacters;
  }
  if (numbers > targetNumbers) {
    numbers = targetNumbers;
  }
  if (uppers > targetUppers) {
    uppers = targetUppers;
  }
  if (specials > targetSpecials) {
    specials = targetSpecials;
  }

  const lengthScore = (length / targetCharacters) * lengthMaxPoints;
  
  const numberScore = numbers / targetNumbers;
  const upperScore = uppers / targetUppers;
  const specialScore = specials / targetSpecials;
  const otherScore = (numberScore + upperScore + specialScore) / 3 * otherMaxPoints;

  const score = lengthScore + otherScore;
  return score;
}
  
function isLetter(char) {
  // The concept of what is a letter is complicated in an international
  // world. Since the overwhelming majority of users are expected to be
  // using English (and most attacks will be making the same assumption),
  // we will treat anything in the ASCII range of 64-90 or 97-122 as a
  // letter
  const code = char.charCodeAt(0);
  //console.log(char, code);
  if ((code >= 64 && code <= 90) || (code >= 97 && code <= 122)) {
    return true;
  }
  return false;
}

function isUpper(char) {
  if (!isLetter(char)) {
    return false;
  }
  if (char === char.toUpperCase()) {
    return true;
  }
  return false;
}

function isNumber(char) {
  const code = char.charCodeAt(0);
  //console.log(char, code);
  if (code >= 48 && code <= 57) {
    return true;
  }
  return false;
}

function isSpecial(char) {
  if (!isLetter(char) && !isNumber(char)) {
    return true;
  }
  return false;
}