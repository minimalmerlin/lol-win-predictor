import { NextResponse } from 'next/server';
import { NextRequest } from 'next/server';

/**
 * Champion Matchup Prediction API Route
 *
 * This endpoint proxies requests to either:
 * 1. External FastAPI backend (if NEXT_PUBLIC_API_URL is set)
 * 2. Vercel Python serverless function in same project (if no external URL)
 * 3. Local FastAPI backend in development (localhost:8000)
 *
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

    // Determine backend URL
    // If NEXT_PUBLIC_API_URL is set, use it (for separate backend deployment)
    // Otherwise, use Vercel serverless functions in the same project
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || process.env.API_URL;
    
    let apiEndpoint: string;
    
    if (backendUrl) {
      // External backend (separate Vercel project or Railway)
      apiEndpoint = `${backendUrl}/api/predict-champion-matchup`;
    } else {
      // Same Vercel project - use serverless functions
      // In development, call FastAPI backend
      if (process.env.NODE_ENV === 'development') {
        apiEndpoint = 'http://localhost:8000/api/predict-champion-matchup';
      } else {
        // Production: Use Vercel serverless function in same project
        // Vercel Python functions in /api are accessible at /api/*
        // We need to construct the full URL from the request
        const requestUrl = new URL(request.url);
        // Use the same origin (same Vercel project)
        apiEndpoint = `${requestUrl.origin}/api/predict-champion-matchup`;
      }
    }

    // Call backend (either external or serverless function)
    const response = await fetch(apiEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Add API key if configured (only for external backends)
        ...(backendUrl && process.env.INTERNAL_API_KEY && {
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
