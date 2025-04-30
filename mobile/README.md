# Mobile - Books App

This is the mobile frontend for the Books App, built with React Native and Expo.

## Features
- React Native (Expo)
- TypeScript support
- Modern UI/UX
- Connects to FastAPI backend

## Project Structure
```
mobile/
  app/                # App screens and navigation
    _layout.tsx       # Main layout/navigation
    HomePage.tsx      # Example home page
  assets/             # Images and fonts
  package.json        # Project dependencies
  tsconfig.json       # TypeScript config
  app.json            # Expo app config
```

## Getting Started

### 1. Install dependencies
```sh
cd mobile
npm install
```

### 2. Start the Expo development server
```sh
npx expo start
```
- Use the QR code to open the app on your device with Expo Go, or run on an emulator.

## Environment Variables
- Add any environment variables to `app.json` or use a `.env` file with [expo-env](https://docs.expo.dev/guides/environment-variables/).

## Connect to Backend
- Update API URLs in your code to point to your backend (FastAPI) server.

## Build for Production
```sh
npx expo build:android   # Android APK
npx expo build:ios       # iOS build (requires Mac)
```

## Screenshots


## License
MIT
