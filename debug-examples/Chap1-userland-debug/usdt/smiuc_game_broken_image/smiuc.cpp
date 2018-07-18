#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <SDL/SDL.h>
#include <SDL/SDL_ttf.h>
int main ( int argc, char** argv )
{
    SDL_Event event;
    bool shotHit=false;
    int pastTime=0,presentTime=0,compteur=0;
    SDL_Rect dstrect, cursorPos, textPos;
    TTF_Font *police = NULL;
    SDL_Color redColor = {255, 0, 0}, whiteColor = {255, 255,255};
    char temps[20] = ""; /* Tableau de char suffisamment grand */
    // initialize SDL video
    if ( SDL_Init( SDL_INIT_VIDEO ) < 0 )
    {
        printf( "Unable to init SDL: %s\n", SDL_GetError() );
        return 1;
    }
    TTF_Init();
    // make sure SDL cleans up before exit
    atexit(SDL_Quit);

    // create a new window
    SDL_Surface* screen = SDL_SetVideoMode(640, 480, 16,
                                           SDL_HWSURFACE|SDL_DOUBLEBUF);
    SDL_WM_SetCaption("smiuc game", NULL);
    /* Chargement de la police */
    police = TTF_OpenFont("fonts/font.TTF", 65);

    if ( !screen )
    {
        printf("Unable to set 640x480 video: %s\n", SDL_GetError());
        return 1;
    }

    // load an image
    SDL_Surface *ActualPinguin=NULL;
    ActualPinguin = SDL_LoadBMP("img/tux-72.bmp");

    //SDL_SetColorKey(bmp,SDL_SRCCOLORKEY,SDL_MapRGB(ActualPinguin->format,255,255,255));
    if (!ActualPinguin)
    {
        printf("Unable to load bitmap: %s\n", SDL_GetError());
        return 1;
    }

    SDL_Surface* cursor_shooter= SDL_LoadBMP("img/game-play-cursor-pointer-shooter-512.bmp");
    SDL_SetColorKey(cursor_shooter,SDL_SRCCOLORKEY,SDL_MapRGB(cursor_shooter->format,255,255,255));
    // centre the bitmap on screen


    dstrect.x = (screen->w - ActualPinguin->w) / 2;
    dstrect.y = (screen->h - ActualPinguin->h) / 2;

    cursorPos.x = (screen->w - cursor_shooter->w) /2;
    cursorPos.y = (screen->h - cursor_shooter->h) /2;
    // program main loop
    bool done = false;
    SDL_ShowCursor(SDL_DISABLE);
    SDL_WarpMouse(ActualPinguin->w/2,ActualPinguin->h/2);
    srand((unsigned) time(NULL));

    sprintf(temps, "Shot hit : %d", compteur);
    SDL_Surface* texte = TTF_RenderText_Shaded(police, temps, redColor,whiteColor);
    textPos.y = screen->h - texte->h;
    while (!done)
    {
        // message processing loop

        SDL_WaitEvent(&event);

        // check for messages
        switch (event.type)
        {
        // exit if the window is closed
        case SDL_QUIT:
            done = true;
            break;
        // check for keypresses
        case SDL_MOUSEMOTION:
            cursorPos.x = event.motion.x - cursor_shooter->w/2;
            cursorPos.y = event.motion.y - cursor_shooter->h/2;
            break;
        case SDL_MOUSEBUTTONDOWN:
            if( (cursorPos.x > dstrect.x) && (cursorPos.x < dstrect.x+ActualPinguin->w) && (cursorPos.y > dstrect.y) && (cursorPos.y < dstrect.y+ActualPinguin->h))
            {

                shotHit=true;
                compteur++;
            }
            break;
        case SDL_KEYDOWN:
        {
            // exit if ESCAPE is pressed
            switch(event.key.keysym.sym)
            {
            case SDLK_ESCAPE:
                done = true;
                break;
            }
            break;

        } // end switch


        }

        presentTime = SDL_GetTicks();
        if(presentTime - pastTime > 1000)
        {
            dstrect.x = cursor_shooter->w + rand() % (screen->w - 100);
            dstrect.y = cursor_shooter->h + rand() % (screen->h - 100 );
            pastTime=presentTime;
        }
        // clear screen

        sprintf(temps, "Shot hit : %d", compteur); /* On écrit dans
        la chaîne "temps" le nouveau temps */
        SDL_FreeSurface(texte); /* On supprime la surface
        précédente */
        texte = TTF_RenderText_Shaded(police, temps,redColor, whiteColor);
        // DRAWING ENDS HERE
        textPos.x = (screen->w - texte->w)/2;

        SDL_FillRect(screen, 0, SDL_MapRGB(screen->format, 255, 255, 255));

        // draw bitmap
        SDL_BlitSurface(ActualPinguin, 0, screen, &dstrect);
        SDL_BlitSurface(cursor_shooter, 0, screen, &cursorPos);

        SDL_BlitSurface(texte, 0, screen, &textPos);
        // finally, update the screen :)
        SDL_Flip(screen);
    } // end main loop

    TTF_CloseFont(police);
    TTF_Quit();
    // free loaded bitmap

    SDL_FreeSurface(ActualPinguin);
    SDL_FreeSurface(cursor_shooter);
    // all is well ;)
    printf("Exited cleanly\n");
    return 0;
}
