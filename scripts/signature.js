import gradient from 'gradient-string';

async function printSignature() {
  try {
    process.env.FORCE_COLOR = '3';

    // Gradiente quente estilo "Open Claude" (Âmbar → Laranja → Coral)
    const warmGradient = gradient(['#fcd34d', '#fb923c', '#f87171']);

    // Cor de texto suave — Bege Almond (#EBD8C3)
    const softText = (txt) => `\x1b[38;2;235;216;195m${txt}\x1b[0m`;

    // Cor dos símbolos decorativos — Coral/Terracotta (#EB926E)
    const starColor = (txt) => `\x1b[38;2;235;146;110m${txt}\x1b[0m`;
    const star = starColor('✦');

    const asciiArt = `
 ___  ___   __    ______  __    __   _______  __      
|   \\/   | |  |  /      ||  |  |  | |   ____||  |     
|  \\  /  | |  | |  ,----'|  |__|  | |  |__   |  |     
|  |\\/|  | |  | |  |     |   __   | |   __|  |  |     
|  |  |  | |  | |  \`----.|  |  |  | |  |____ |  \`----.
|__|  |__| |__|  \\______||__|  |__| |_______||_______|`;

    console.log('\n' + softText('SOFTWARE DESENVOLVIDO POR:'));
    console.log(warmGradient.multiline(asciiArt));
    console.log(`          ${star} ${softText('MICHEL SOFTWARES - SOLUÇÕES MODERNAS')} ${star}`);
    console.log(`           ${star} ${softText('MichelAraujo.exe@gmail.com')} ${star}`);
    console.log('\n' + softText('"Tudo o que fizerem, façam de todo o coração, como para o Senhor, e não para os homens,"'));
    console.log('\t' + softText('Colossenses 3:23\n'));

  } catch (err) {
    // Fallback sem cores
    console.log('\n--- TEXTO PARA VOZ STUDIO | EDGE-TTS - DESENVOLVEDOR ---\n');
  }
}

printSignature();
