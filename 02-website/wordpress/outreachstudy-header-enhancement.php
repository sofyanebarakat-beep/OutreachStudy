<?php
/**
 * Outreach Study global header enhancement.
 * Loaded by the EdCare theme's functions.php.
 */

if (!defined('ABSPATH')) {
    exit;
}

function outreachstudy_header_enhancement_assets()
{
    $asset_file = get_template_directory() . '/inc/outreachstudy-header-enhancement.html';

    if (is_readable($asset_file)) {
        echo file_get_contents($asset_file); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
    }
}
add_action('wp_head', 'outreachstudy_header_enhancement_assets', 99);
