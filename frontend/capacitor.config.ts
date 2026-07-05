import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'ru.ssilurs.tocooklist',
  appName: 'To Cook List',
  webDir: 'dist',
  android: {
    allowMixedContent: false,
    captureInput: true,
    webContentsDebuggingEnabled: true  // Allows chrome://inspect debugging
  }
};

export default config;
