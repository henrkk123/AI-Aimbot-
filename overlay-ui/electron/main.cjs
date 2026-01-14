const { app, BrowserWindow, ipcMain, screen } = require('electron');
const path = require('path');
const isDev = process.env.NODE_ENV === 'development';

let mainWindow;

function createWindow() {
    // Use 'bounds' to get the full screen size (including taskbar area)
    // This is critical for game overlays to cover the entire resolution.
    const { width, height } = screen.getPrimaryDisplay().bounds;

    mainWindow = new BrowserWindow({
        width: width,
        height: height,
        x: 0,
        y: 0,
        frame: false,
        transparent: true,
        alwaysOnTop: true,
        hasShadow: false,
        resizable: false,
        movable: false, // Don't let users drag it
        focusable: true, // Need focus for menu
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false, // Simplify for this prototype
            backgroundThrottling: false // Important for smooth animation
        }
    });

    // Make it full screen overlay
    mainWindow.setSimpleFullScreen(true);

    // Mac specific: Level usually needs to be higher to float over games
    // 'screen-saver' level is highest on Mac
    mainWindow.setVisibleOnAllWorkspaces(true, { visibleOnFullScreen: true });
    mainWindow.setAlwaysOnTop(true, 'screen-saver');

    // Load App
    const startUrl = isDev
        ? 'http://localhost:5173'
        : `file://${path.join(__dirname, '../dist/index.html')}`;

    mainWindow.loadURL(startUrl);

    // Default: Pass clicks through to the game
    // logic: If mouse is over a UI element (Menu), we trap it.
    // But detection is hard. 
    // Simple approach: IPC toggles.
    mainWindow.setIgnoreMouseEvents(true, { forward: true });

    // Event to toggle click-through
    ipcMain.on('set-ignore-mouse-events', (event, ignore, options) => {
        const win = BrowserWindow.fromWebContents(event.sender);
        win.setIgnoreMouseEvents(ignore, { forward: true });
    });

    if (isDev) {
        // mainWindow.webContents.openDevTools({ mode: 'detach' });
    }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
