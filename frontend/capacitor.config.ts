import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'ru.ssilurs.tocooklist',
  appName: 'To Cook List',
  webDir: 'dist',
  server: {
    // All API requests in APK go to production server
    url: 'https://tocook.ssilurs.ru',
    cleartext: false
  },
  android: {
    allowMixedContent: false,
    captureInput: true,
    webContentsDebuggingEnabled: false
  }
};

export default config;
