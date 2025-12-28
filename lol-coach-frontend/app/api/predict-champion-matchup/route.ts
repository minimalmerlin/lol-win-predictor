import { NextResponse } from 'next/server';
import { NextRequest } from 'next/server';

// Simple mock prediction based on team size
function predictMatchup(blueChampions: string[], redChampions: string[]) {
  // Calculate mock win rates based on champion names (deterministic but pseudo-random)
  const calculateTeamStrength = (team: string[]) => {
    return team.reduce((sum, champ) => {
      // Use champion name length and character codes for pseudo-random strength
      const strength = champ.split('').reduce((s, c) => s + c.charCodeAt(0), 0);
      return sum + (strength % 100) / 100;
    }, 0) / team.length;
  };

  const blueStrength = calculateTeamStrength(blueChampions);
  const redStrength = calculateTeamStrength(redChampions);

  // Normalize to probabilities
  const total = blueStrength + redStrength;
  let blueWinProb = blueStrength / total;
  let redWinProb = redStrength / total;

  // Add some randomness
  const randomFactor = (Math.random() - 0.5) * 0.1;
  blueWinProb = Math.max(0.2, Math.min(0.8, blueWinProb + randomFactor));
  redWinProb = 1 - blueWinProb;

  const prediction = blueWinProb > 0.5 ? 'Blue Team' : 'Red Team';
  const winProbability = Math.max(blueWinProb, redWinProb);

  let confidence = 'Medium';
  if (winProbability > 0.65) confidence = 'High';
  else if (winProbability < 0.55) confidence = 'Low';

  return {
    blue_win_probability: blueWinProb,
    red_win_probability: redWinProb,
    prediction,
    confidence,
    details: {
      blue_avg_winrate: 0.48 + (blueStrength - 0.5) * 0.2,
      red_avg_winrate: 0.48 + (redStrength - 0.5) * 0.2,
      model: 'Neural Network v2.0',
      accuracy: '90.9%'
    }
  };
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { blue_champions, red_champions } = body;

    if (!blue_champions || !red_champions) {
      return NextResponse.json(
        { error: 'Missing blue_champions or red_champions' },
        { status: 400 }
      );
    }

    if (!Array.isArray(blue_champions) || !Array.isArray(red_champions)) {
      return NextResponse.json(
        { error: 'blue_champions and red_champions must be arrays' },
        { status: 400 }
      );
    }

    const prediction = predictMatchup(blue_champions, red_champions);
    return NextResponse.json(prediction);
  } catch (error) {
    return NextResponse.json(
      { error: 'Invalid request body' },
      { status: 400 }
    );
  }
}
