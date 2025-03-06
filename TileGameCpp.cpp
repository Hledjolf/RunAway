#include <SDL.h>
#include <SDL_image.h>
#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <filesystem>
#include <random>

const int TILE_SIZE = 16;
const int MAP_WIDTH = 50;
const int MAP_HEIGHT = 50;
const int INFO_PANEL_HEIGHT = 50;
const std::string TILESETS_FOLDER = "tilesets";

class Tile {
public:
    std::string tile_type;
    bool walkable;
    SDL_Texture* image;

    Tile(const std::string& type, bool walk, SDL_Texture* img)
        : tile_type(type), walkable(walk), image(img) {}
};

std::map<std::string, SDL_Texture*> loadTilesets(SDL_Renderer* renderer, const std::string& folder) {
    std::map<std::string, SDL_Texture*> tiles;
    for (const auto& entry : std::filesystem::directory_iterator(folder)) {
        if (entry.path().extension() == ".webp") {
            SDL_Surface* surface = IMG_Load(entry.path().string().c_str());
            SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer, surface);
            SDL_FreeSurface(surface);
            std::string tile_type = entry.path().stem().string();
            tiles[tile_type] = texture;
        }
    }
    return tiles;
}

std::vector<std::vector<Tile>> createMap(const std::map<std::string, SDL_Texture*>& tiles) {
    std::vector<std::vector<Tile>> map_grid;
    std::vector<std::string> tile_types;
    for (const auto& pair : tiles) {
        tile_types.push_back(pair.first);
    }

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, tile_types.size() - 1);

    for (int y = 0; y < MAP_HEIGHT; ++y) {
        std::vector<Tile> row;
        for (int x = 0; x < MAP_WIDTH; ++x) {
            std::string tile_type = tile_types[dis(gen)];
            bool walkable = (tile_type != "water");
            row.emplace_back(tile_type, walkable, tiles.at(tile_type));
        }
        map_grid.push_back(row);
    }
    return map_grid;
}

void renderMap(SDL_Renderer* renderer, const std::vector<std::vector<Tile>>& map_grid) {
    for (int y = 0; y < MAP_HEIGHT; ++y) {
        for (int x = 0; x < MAP_WIDTH; ++x) {
            SDL_Rect dstRect = { x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE };
            SDL_RenderCopy(renderer, map_grid[y][x].image, nullptr, &dstRect);
        }
    }
}

std::string getTileType(int mouseX, int mouseY, const std::vector<std::vector<Tile>>& map_grid) {
    int gridX = mouseX / TILE_SIZE;
    int gridY = mouseY / TILE_SIZE;
    if (gridX >= 0 && gridX < MAP_WIDTH && gridY >= 0 && gridY < MAP_HEIGHT) {
        return map_grid[gridY][gridX].tile_type;
    }
    return "None";
}

void drawInfoPanel(SDL_Renderer* renderer, TTF_Font* font, const std::string& tile_type) {
    SDL_Color textColor = { 255, 255, 255, 255 };
    std::string text = "Tile Type: " + tile_type;

    SDL_Surface* textSurface = TTF_RenderText_Solid(font, text.c_str(), textColor);
    SDL_Texture* textTexture = SDL_CreateTextureFromSurface(renderer, textSurface);

    SDL_Rect textRect = { 10, MAP_HEIGHT * TILE_SIZE + 10, textSurface->w, textSurface->h };
    SDL_FreeSurface(textSurface);

    SDL_Rect panelRect = { 0, MAP_HEIGHT * TILE_SIZE, MAP_WIDTH * TILE_SIZE, INFO_PANEL_HEIGHT };
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
    SDL_RenderFillRect(renderer, &panelRect);

    SDL_RenderCopy(renderer, textTexture, nullptr, &textRect);
    SDL_DestroyTexture(textTexture);
}

int main(int argc, char* argv[]) {
    if (SDL_Init(SDL_INIT_VIDEO) < 0 || TTF_Init() < 0) {
        std::cerr << "SDL/TTF could not initialize! SDL_Error: " << SDL_GetError() << std::endl;
        return 1;
    }

    SDL_Window* window = SDL_CreateWindow("Tile Map", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
                                          MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE + INFO_PANEL_HEIGHT, SDL_WINDOW_SHOWN);
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    TTF_Font* font = TTF_OpenFont("path/to/font.ttf", 36);
    if (!font) {
        std::cerr << "Failed to load font! TTF_Error: " << TTF_GetError() << std::endl;
        return 1;
    }

    auto tiles = loadTilesets(renderer, TILESETS_FOLDER);
    auto map_grid = createMap(tiles);

    bool quit = false;
    SDL_Event e;
    while (!quit) {
        while (SDL_PollEvent(&e) != 0) {
            if (e.type == SDL_QUIT) {
                quit = true;
            }
        }

        int mouseX, mouseY;
        SDL_GetMouseState(&mouseX, &mouseY);
        std::string tile_type = getTileType(mouseX, mouseY, map_grid);

        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        renderMap(renderer, map_grid);
        drawInfoPanel(renderer, font, tile_type);

        SDL_RenderPresent(renderer);
    }

    TTF_CloseFont(font);
    font = nullptr;

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);

    TTF_Quit();
    SDL_Quit();

    return 0;
}