import { useState, useEffect, useRef } from 'react';

/**
 * Hook that gradually reveals text character-by-character for a typewriter effect.
 *
 * @param targetText - The full text to reveal
 * @param isActive - Whether the typewriter effect should be active (typically messageIsStreaming && isLastMessage)
 * @param charsPerFrame - Number of characters to reveal per animation frame (default: 3)
 * @returns { displayedText, isRevealing, cursorVisible }
 */
export function useTypewriter(
  targetText: string,
  isActive: boolean,
  charsPerFrame: number = 3
): { displayedText: string; isRevealing: boolean } {
  const [displayedLength, setDisplayedLength] = useState(0);
  const animationRef = useRef<number | null>(null);
  const lastTargetRef = useRef(targetText);

  useEffect(() => {
    // If not active, show full text immediately
    if (!isActive) {
      setDisplayedLength(targetText.length);
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
        animationRef.current = null;
      }
      return;
    }

    // If target text changed (new content arrived), keep revealing
    if (targetText !== lastTargetRef.current) {
      lastTargetRef.current = targetText;
    }

    // Animation function
    const animate = () => {
      setDisplayedLength((current) => {
        if (current >= targetText.length) {
          animationRef.current = null;
          return current;
        }
        // Reveal more characters
        const next = Math.min(current + charsPerFrame, targetText.length);
        return next;
      });

      // Continue animation if not caught up
      animationRef.current = requestAnimationFrame(animate);
    };

    // Start animation if we're behind
    if (displayedLength < targetText.length && !animationRef.current) {
      animationRef.current = requestAnimationFrame(animate);
    }

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
        animationRef.current = null;
      }
    };
  }, [targetText, isActive, charsPerFrame, displayedLength]);

  const displayedText = targetText.slice(0, displayedLength);
  const isRevealing = isActive && displayedLength < targetText.length;

  return { displayedText, isRevealing };
}
