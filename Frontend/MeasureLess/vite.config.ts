import path from "path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig(() => ({
    plugins: [react(), tailwindcss()],
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"),
        },
    },
    server: {
        host: true,
        port: 5173,
        allowedHosts: [
            "clothing-app-2n6a.onrender.com"
        ],
        proxy: {
            '/api': {
                target: 'clothing-app-wuff:5000',
                changeOrigin: true,
                secure: false,
            }
        }
    },
}));

