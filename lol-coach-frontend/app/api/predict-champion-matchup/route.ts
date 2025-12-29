import { NextResponse } from 'next/server';
import { NextRequest } from 'next/server';

/**
 * Champion Matchup Prediction API Route
 *
 * This endpoint proxies requests to the FastAPI backend for real ML predictions.
 * No mock data - all predictions come from the trained scikit-learn models.
 */

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { blue_champions, red_champions } = body;

    // Validate input
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

    // Get backend URL from environment with fallback for local development
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || process.env.API_URL || 'http://localhost:8000';

    if (!backendUrl) {
      return NextResponse.json(
        {
          error: 'Backend API URL not configured',
          details: 'Please set NEXT_PUBLIC_API_URL or API_URL environment variable, or start the backend on http://localhost:8000'
        },
        { status: 503 }
      );
    }

    // Call real FastAPI backend
    const response = await fetch(`${backendUrl}/api/predict-champion-matchup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Add API key if configured
        ...(process.env.INTERNAL_API_KEY && {
          'X-INTERNAL-API-KEY': process.env.INTERNAL_API_KEY
        })
      },
      body: JSON.stringify({
        blue_champions,
        red_champions
      })
    });

    if (!response.ok) {
      let errorDetail = 'Backend prediction failed';
      try {
        const errorData = await response.json();
        errorDetail = errorData.detail || errorData.error || errorData.message || errorDetail;
      } catch {
        // If JSON parsing fails, try text
        try {
          const errorText = await response.text();
          errorDetail = errorText || errorDetail;
        } catch {
          errorDetail = `HTTP ${response.status}: ${response.statusText}`;
        }
      }
      
      console.error('Backend API error:', response.status, errorDetail);

      return NextResponse.json(
        {
          error: errorDetail,
          status: response.status,
          details: `Backend returned status ${response.status}`
        },
        { status: response.status }
      );
    }

    const prediction = await response.json();
    return NextResponse.json(prediction);

  } catch (error) {
    console.error('Prediction API error:', error);

    // Distinguish between different error types
    if (error instanceof TypeError && error.message.includes('fetch')) {
      return NextResponse.json(
        {
          error: 'Cannot connect to backend API',
          details: 'Please ensure the FastAPI backend is running'
        },
        { status: 503 }
      );
    }

    return NextResponse.json(
      {
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
